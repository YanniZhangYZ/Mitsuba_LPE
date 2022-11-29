from __future__ import annotations # Delayed parsing of type annotations

import drjit as dr
import mitsuba as mi

from mitsuba.python.ad.integrators.common import RBIntegrator, mis_weight
from LPE_Engine.drjit_utils import DrJitDFA

class PathMatsDFAIntegrator(RBIntegrator):
    def __init__(self, props):
        super().__init__(props)
        regex = props['lpe']
        # regex = "AE"
        # regex = "DE"
        # regex = "GE"
        # regex = "G"
        # regex = "E"
        print(regex)
        self.dfa = DrJitDFA(regex)


    def sample(self,
               mode: dr.ADMode,
               scene: mi.Scene,
               sampler: mi.Sampler,
               ray: mi.Ray3f,
               δL: Optional[mi.Spectrum],
               state_in: Optional[mi.Spectrum],
               active: mi.Bool,
               **kwargs # Absorbs unused arguments
    ) -> Tuple[mi.Spectrum,
               mi.Bool, mi.Spectrum]:
        """
        See ``ADIntegrator.sample()`` for a description of this interface and
        the role of the various parameters and return values.
        """

        dr.set_flag(dr.JitFlag.LoopRecord, False)


        # Standard BSDF evaluation context for path tracing
        bsdf_ctx = mi.BSDFContext()

        # --------------------- Configure loop state ----------------------

        # Copy input arguments to avoid mutating the caller's state
        ray = mi.Ray3f(dr.detach(ray))
        depth = mi.UInt32(0)                          # Depth of current vertex
        L = mi.Spectrum(0)    # Radiance accumulator
        δL = mi.Spectrum(δL if δL is not None else 0) # Differential/adjoint radiance
        β = mi.Spectrum(1)                            # Path throughput weight
        η = mi.Float(1)                               # Index of refraction
        active = mi.Bool(active)                      # Active SIMD lanes

        # Variables caching information from the previous bounce
        prev_si         = dr.zeros(mi.SurfaceInteraction3f)
        prev_bsdf_pdf   = mi.Float(1.0)
        prev_bsdf_delta = mi.Bool(True)

        # DFA
        batch_size = dr.width(ray)
        prev_states = dr.zeros(mi.Int32, batch_size) + 1


        # Record the following loop in its entirety
        loop = mi.Loop(name="Mats DFA (%s)" % mode.name,
                       state=lambda: (sampler, ray, depth, L, δL, β, η, active,
                                      prev_si, prev_bsdf_pdf, prev_bsdf_delta,prev_states))

        # Specify the max. number of loop iterations (this can help avoid
        # costly synchronization when when wavefront-style loops are generated)
        loop.set_max_iterations(self.max_depth)



        while loop(active):
            # Compute a surface interaction that tracks derivatives arising
            # from differentiable shape parameters (position, normals, etc.)
            # In primal mode, this is just an ordinary ray tracing operation.
            
            si = scene.ray_intersect(ray,
                                    ray_flags=mi.RayFlags.All,
                                    coherent=dr.eq(depth, 0))

            # Get the BSDF, potentially computes texture-space differentials
            bsdf = si.bsdf(ray)

            # ---------------------- Direct emission ----------------------

            # Compute MIS weight for emitter sample from previous bounce
            ds = mi.DirectionSample3f(scene, si=si, ref=prev_si)

            # ADD EMITTER EVENT FOR dr.neq(ds.emitter, None) -> TRANSITION()
            curr_states = prev_states

            emitter_mask = dr.neq(si.emitter(scene), None)
            events =self.dfa.create_emitter_events(emitter_mask)
            temp_curr_states = self.dfa.transition(curr_states, events)
            accept_mask = self.dfa.get_accept_mask(temp_curr_states)

            Le = dr.select(accept_mask, β * ds.emitter.eval(si),0)


            # Should we continue tracing to reach one more vertex?
            active_next = (depth + 1 < self.max_depth) & si.is_valid()

            #DFA
            # active_next = active_next & dr.neq(True,kill_mask)

            # ------------------ Detached BSDF sampling -------------------

            bsdf_sample, bsdf_weight = bsdf.sample(bsdf_ctx, si,
                                                   sampler.next_1d(),
                                                   sampler.next_2d(),
                                                   active_next)

            # ---- Update loop variables based on current interaction -----

            # L = (L + Le + Lr_dir)
            L = (L + Le)
            ray = si.spawn_ray(si.to_world(bsdf_sample.wo))
            η *= bsdf_sample.eta
            β *= bsdf_weight


            # ADD bsdf_sample.sample_type EVENT -> TRANSITION()

            bsdf_events0, bsdf_events1= self.dfa.flags_to_events(bsdf_sample.sampled_type)
            curr_states = self.dfa.transition(curr_states, bsdf_events0)
            curr_states = self.dfa.transition(curr_states, bsdf_events1)
            kill_mask = self.dfa.get_kill_mask(curr_states)

            # Information about the current vertex needed by the next iteration

            prev_si = dr.detach(si, True)
            prev_bsdf_pdf = bsdf_sample.pdf
            prev_bsdf_delta = mi.has_flag(bsdf_sample.sampled_type, mi.BSDFFlags.Delta)
            

            # -------------------- Stopping criterion ---------------------

            # Don't run another iteration if the throughput has reached zero
            β_max = dr.max(β)
            active_next &= dr.neq(β_max, 0)

            # Russian roulette stopping probability (must cancel out ior^2
            # to obtain unitless throughput, enforces a minimum probability)
            rr_prob = dr.minimum(β_max * η**2, .95)

            # Apply only further along the path since, this introduces variance
            rr_active = depth >= self.rr_depth
            β[rr_active] *= dr.rcp(rr_prob)
            rr_continue = sampler.next_1d() < rr_prob
            active_next &= ~rr_active | rr_continue


            depth[si.is_valid()] += 1
            active = active_next

            #DFA
            active = active & ~kill_mask
            prev_states = curr_states
            print(active == False)

        return (
            L , # Radiance/differential radiance
            dr.neq(depth, 0),    # Ray validity flag for alpha blending
            L                    # State for the differential phase
        )