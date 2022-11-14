from __future__ import annotations  # Delayed parsing of type annotations

import drjit as dr
import mitsuba as mi

from mitsuba.python.ad.integrators.common import ADIntegrator, mis_weight
from LPE_Engine.drjit_utils import DrJitDFA
from LPE_Engine.prototype.lexical_analysis import Event
from LPE_Engine.prototype.lexical_analysis import StateUtils


class SimpleDFAIntegrator(ADIntegrator):
    def __init__(self, props):
        super().__init__(props)
        regex = "."
        # regex = "DE"
        # regex = "SE"
        # regex = "GE"
        self.dfa = DrJitDFA(regex)
        # self.dfa = dfa
        # event_batch = events[:, i]
        # enums_tmp = jitDFA.g.check_translate_event_batch_simple(event_batch)
        # enums = mi.Int32(enums_tmp)
        # # print("After " + str(i+1)+"th event")
        # light_mask = dr.eq(Event.Emitter.value, enums)
        # next_states = jitDFA.transition(curr_states, enums, light_mask)

        # # restore state that hit the light, aka skip state transition when hit light
        # next_states = dr.select(light_mask, curr_states, next_states)
        # print(next_states)

        # curr_states = next_states

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

        # INITIALIZE STATE to CAMERA
        curr_states = dr.zeros(mi.Int32, dr.width(ray)) + 1

        # ---------------------- Direct emission ----------------------

        si = scene.ray_intersect(ray, active)
        # ADD EMITTER EVENT FOR dr.neq(si.emitter, 0) -> TRANSITION()
        light_mask = dr.neq(si.emitter(scene), None)
        # events = self.creat_emitter_events(dr.width(ray), light_mask)
        # direct_accept_mask, direct_kill_mask, curr_states = self.hit_light_transition(
        #     events, light_mask, curr_states)

        # print(dr.eq(curr_states, 1))

        # Differentiable evaluation of intersected emitter / envmap
        L += si.emitter(scene).eval(si)  # MASKED FOR ACCEPTED STATES
        # L += dr.select(direct_accept_mask, si.emitter(scene).eval(si), 0)

        # ------------------ BSDF sampling -------------------

        # Should we continue tracing to reach one more vertex?
        active_next = si.is_valid()
        active_next = active_next
        bsdf = si.bsdf(ray)

        # BSDF sample
        bsdf_sample, bsdf_weight = bsdf.sample(bsdf_ctx, si, sampler.next_1d(active_next),
                                               sampler.next_2d(active_next), active_next)
        # Spawn a semi-infinite ray towards the given direction
        ray_bsdf = si.spawn_ray(si.to_world(bsdf_sample.wo))
        active_bsdf = active_next & dr.any(dr.neq(bsdf_weight, 0.0))

        # ADD bsdf_sample.sample_type EVENT -> TRANSITION()
        bsdf_events = self.flags_to_events(bsdf_sample.sampled_type)

        # Illumination
        si_bsdf = scene.ray_intersect(ray_bsdf, active_bsdf)
        L_bsdf = si_bsdf.emitter(scene).eval(si_bsdf, active_bsdf)

        # ADD EMITTER EVENT FOR dr.neq(si.emitter, 0) -> TRANSITION()
        # light_mask = dr.neq(si_bsdf.emitter(scene), None)
        # events = self.creat_emitter_events(dr.width(ray), light_mask)
        # accept_mask, kill_mask, curr_states = self.hit_light_transition(
        #     events, light_mask, curr_states)
        # events = self.creat_emitter_events(dr.width(ray), light_mask)
        # next_states = self.dfa.transition(curr_states, events, light_mask)
        # curr_states = dr.select(light_mask, next_states, curr_states)
        # accept_mask = dr.eq(curr_states, StateUtils.ACCEPT_STATE.value)
        # kill_mask = dr.eq(curr_states, StateUtils.KILLED_STATE.value)

        # L += dr.select(accept_mask, L_bsdf * bsdf_weight, 0)

        L += L_bsdf * bsdf_weight  # MASKED FOR ACCEPTED STATES

        return L, active, None

    def hit_light_transition(self, events, light_mask, curr):
        next = self.dfa.transition(curr, events, light_mask)
        curr = dr.select(light_mask, next, curr)

        accept_mask = dr.eq(curr, StateUtils.ACCEPT_STATE.value)
        kill_mask = dr.eq(curr, StateUtils.KILLED_STATE.value)

        return accept_mask, kill_mask, curr

    def creat_emitter_events(self, batch_width, light_mask):
        events = dr.zeros(mi.Int32, dr.width(batch_width)) + \
            Event.NO_EVENT.value
        events = dr.select(light_mask, Event.Emitter.value, events)
        return events

    def flags_to_events(self, flags):
        flag_list = {mi.BSDFFlags.Reflection: Event.Reflection.value,
                     mi.BSDFFlags.Diffuse: Event.Diffuse.value,
                     mi.BSDFFlags.Transmission: Event.Transmission.value,
                     mi.BSDFFlags.Glossy: Event.Glossy.value,
                     mi.BSDFFlags.Delta: Event.Delta.value}
        events = dr.zeros(mi.Int32, dr.width(flags)) + Event.NO_EVENT.value
        for f, e in flag_list.items():
            mask = mi.has_flag(flags, f)
            events = dr.select(mask, e, events)
        return events

        # mi.register_integrator(
        #     "simple_reparam", lambda props: SimpleIntegrator(props))
