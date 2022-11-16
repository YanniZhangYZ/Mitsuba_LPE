from __future__ import annotations  # Delayed parsing of type annotations

import drjit as dr
import mitsuba as mi

from mitsuba.python.ad.integrators.common import ADIntegrator, mis_weight


class SimpleMISIntegrator(ADIntegrator):

    def __init__(self, props):
        super().__init__(props)

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
    
        bsdf_ctx = mi.BSDFContext()
        L = mi.Spectrum(0)

        # ---------------------- Direct emission ----------------------

        pi = scene.ray_intersect_preliminary(ray, active)
        si = pi.compute_surface_interaction(ray)

        # Differentiable evaluation of intersected emitter / envmap
        L += si.emitter(scene).eval(si)

        # ------------------ Emitter sampling -------------------

        # Should we continue tracing to reach one more vertex?
        active_next = si.is_valid()
        # Get the BSDF. Potentially computes texture-space differentials.
        bsdf = si.bsdf(ray)

        # Detached emitter sample
        active_em = active_next & mi.has_flag(
            bsdf.flags(), mi.BSDFFlags.Smooth)
        
        ds, weight_em = scene.sample_emitter_direction(
                si, sampler.next_2d(), True, active_em)
        active_em &= dr.neq(ds.pdf, 0.0)
        
        # Reparameterize the ray
        ray_em_det = 1.0
        
        # Compute MIS
        wo = si.to_local(ds.d)
        bsdf_value_em, bsdf_pdf_em = bsdf.eval_pdf(bsdf_ctx, si, wo, active_em)
        mis_em = dr.select(ds.delta, 1.0, mis_weight(ds.pdf, bsdf_pdf_em))

        L += bsdf_value_em * weight_em * ray_em_det * mis_em

        # ------------------ BSDF sampling -------------------

        # Detached BSDF sample

        bsdf_sample, bsdf_weight = bsdf.sample(bsdf_ctx, si, sampler.next_1d(active_next),
                                                sampler.next_2d(active_next), active_next)
        ray_bsdf = si.spawn_ray(si.to_world(bsdf_sample.wo))
        active_bsdf = active_next & dr.any(dr.neq(bsdf_weight, 0.0))

        # Reparameterize the ray
        ray_bsdf_det = 1.0
        
        # Illumination
        si_bsdf = scene.ray_intersect(ray_bsdf, active_bsdf)
        L_bsdf = si_bsdf.emitter(scene).eval(si_bsdf, active_bsdf)

        # Compute MIS
        ds = mi.DirectionSample3f(scene, si_bsdf, si)
        delta = mi.has_flag(bsdf_sample.sampled_type, mi.BSDFFlags.Delta)
        emitter_pdf = scene.pdf_emitter_direction(
            si, ds, active_bsdf & ~delta)
        mis_bsdf = mis_weight(bsdf_sample.pdf, emitter_pdf)

        L += L_bsdf * bsdf_weight * ray_bsdf_det * mis_bsdf

        return L, active, None