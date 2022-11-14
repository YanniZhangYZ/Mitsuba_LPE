from __future__ import annotations  # Delayed parsing of type annotations

import drjit as dr
import mitsuba as mi

from mitsuba.python.ad.integrators.common import ADIntegrator


class SimpleFlagIntegrator(ADIntegrator):
    r"""
    .. _integrator-direct_reparam:

    Reparameterized Direct Integrator (:monosp:`direct_reparam`)
    -------------------------------------------------------------

    .. pluginparameters::

     * - reparam_max_depth
       - |int|
       - Specifies the longest path depth for which the reparameterization
         should be enabled (maximum 2 for this integrator). A value of 1
         will only produce visibility gradients for directly visible shapes
         while a value of 2 will also account for shadows. (Default: 2)

     * - reparam_rays
       - |int|
       - Specifies the number of auxiliary rays to be traced when performing the
         reparameterization. (Default: 16)

     * - reparam_kappa
       - |float|
       - Specifies the kappa parameter of the von Mises Fisher distribution used
         to sample auxiliary rays.. (Default: 1e5)

     * - reparam_exp
       - |float|
       - Power exponent applied on the computed harmonic weights in the
         reparameterization. (Default: 3.0)

     * - reparam_antithetic
       - |bool|
       - Should antithetic sampling be enabled to improve convergence when
         sampling the auxiliary rays. (Default: False)

    This plugin implements a reparameterized direct illumination integrator.

    It is functionally equivalent with `prb_reparam` when `max_depth` and
    `reparam_max_depth` are both set to be 2. But since direct illumination
    tasks only have two ray segments, the overhead of relying on radiative
    backpropagation is non-negligible. This implementation builds on the
    traditional ADIntegrator that does not require two passes during
    gradient traversal.

    .. tabs::

        .. code-tab:: python

            'type': 'direct_reparam',
            'reparam_rays': 8
    """

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
        """
        See ``ADIntegrator.sample()`` for a description of this interface and
        the role of the various parameters and return values.
        """

        bsdf_ctx = mi.BSDFContext()
        L = mi.Spectrum(0)

        # ---------------------- Direct emission ----------------------

        pi = scene.ray_intersect_preliminary(ray, active)
        si = pi.compute_surface_interaction(ray)

        # Differentiable evaluation of intersected emitter / envmap
        L += si.emitter(scene).eval(si)

        # ------------------ BSDF sampling -------------------

        # Should we continue tracing to reach one more vertex?
        active_next = si.is_valid()
        bsdf = si.bsdf(ray)

        # Detached BSDF sample
        bsdf_sample, bsdf_weight = bsdf.sample(bsdf_ctx, si, sampler.next_1d(active_next),
                                               sampler.next_2d(active_next), active_next)
        ray_bsdf = si.spawn_ray(si.to_world(bsdf_sample.wo))
        active_bsdf = active_next & dr.any(dr.neq(bsdf_weight, 0.0))

        # --------------try to tell transmission/ reflection/ diffuse ------------
        reflection_flag = mi.has_flag(
            bsdf_sample.sampled_type, mi.BSDFFlags.Reflection)
        transmission_flag = mi.has_flag(
            bsdf_sample.sampled_type, mi.BSDFFlags.Transmission)
        delta_flag = mi.has_flag(
            bsdf_sample.sampled_type, mi.BSDFFlags.Transmission)
        glossy_flag = mi.has_flag(
            bsdf_sample.sampled_type, mi.BSDFFlags.Glossy)
       # ----------------------------------------------------------------

        active_filter = active_bsdf & glossy_flag
        #  active_filter = active_bsdf & transmission_flag

        # Illumination
        si_bsdf = scene.ray_intersect(ray_bsdf, active_filter)
        L_bsdf = si_bsdf.emitter(scene).eval(si_bsdf, active_filter)

        L += L_bsdf * bsdf_weight

        return L, active_filter, None
