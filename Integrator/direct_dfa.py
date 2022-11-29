from __future__ import annotations  # Delayed parsing of type annotations

import drjit as dr
import mitsuba as mi

from mitsuba.python.ad.integrators.common import ADIntegrator, mis_weight
from LPE_Engine.drjit_utils import DrJitDFA
from LPE_Engine.prototype.lexical_analysis import Event
from LPE_Engine.prototype.lexical_analysis import StateUtils


class DirectDFAIntegrator(ADIntegrator):
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
               reparam: Optional[
                   Callable[[mi.Ray3f, mi.Bool],
                            Tuple[mi.Ray3f, mi.Float]]],
               active: mi.Bool,
               **kwargs  # Absorbs unused arguments
               ) -> Tuple[mi.Spectrum, mi.Bool, mi.Spectrum]:
        """
        See ``ADIntegrator.sample()`` for a description of this interface and
        the role of the various parameters and return values.
        """
        batch_size = dr.width(ray)

        bsdf_ctx = mi.BSDFContext()
        L = mi.Spectrum(0)

        # INITIALIZE STATE to CAMERA
        curr_states = dr.zeros(mi.Int32, batch_size) + 1

        # ---------------------- Direct emission ----------------------

        si = scene.ray_intersect(ray, active)

        # ADD EMITTER EVENT FOR dr.neq(si.emitter, 0) -> TRANSITION()

        emitter_mask = dr.neq(si.emitter(scene), None)
        events =self.dfa.create_emitter_events(emitter_mask)
        temp_curr_states = self.dfa.transition(curr_states, events)
        accept_mask = self.dfa.get_accept_mask(temp_curr_states)

        # Differentiable evaluation of intersected emitter / envmap
        L += dr.select(accept_mask, si.emitter(scene).eval(si),0)


        # ------------------ BSDF sampling -------------------

        # Should we continue tracing to reach one more vertex?
        active_next = si.is_valid()
        # active_next = active_next & dr.neq(True,kill_mask)

        bsdf = si.bsdf(ray)

        # BSDF sample
        bsdf_sample, bsdf_weight = bsdf.sample(bsdf_ctx, si, sampler.next_1d(active_next),
                                               sampler.next_2d(active_next), active_next)
        # Spawn a semi-infinite ray towards the given direction
        ray_bsdf = si.spawn_ray(si.to_world(bsdf_sample.wo))
        active_bsdf = active_next & dr.any(dr.neq(bsdf_weight, 0.0))



        # ADD bsdf_sample.sample_type EVENT -> TRANSITION()
        bsdf_events0, bsdf_events1= self.dfa.flags_to_events(bsdf_sample.sampled_type)
        curr_states = self.dfa.transition(curr_states, bsdf_events0)
        curr_states = self.dfa.transition(curr_states, bsdf_events1)
        kill_mask = self.dfa.get_kill_mask(curr_states)
        active_filter = active_bsdf & ~kill_mask

        # Illumination
        si_bsdf = scene.ray_intersect(ray_bsdf, active_filter)
        L_bsdf = si_bsdf.emitter(scene).eval(si_bsdf, active_filter)

        # ADD EMITTER EVENT FOR dr.neq(si.emitter, 0) -> TRANSITION()
        emitter_mask = dr.neq(si_bsdf.emitter(scene), None)
        events = self.dfa.create_emitter_events(emitter_mask)
        next_states = self.dfa.transition(curr_states, events)
        curr_states = next_states
        accept_mask = self.dfa.get_accept_mask(curr_states)

        L += dr.select(accept_mask, L_bsdf * bsdf_weight, 0)

        # L += L_bsdf * bsdf_weight  # MASKED FOR ACCEPTED STATES

        return L, active, None
