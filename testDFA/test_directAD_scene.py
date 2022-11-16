import drjit as dr
import mitsuba as mi
# from mitsuba.python.ad.integrators.direct_reparam import DirectReparamIntegrator
from mitsuba.python.ad.integrators import direct_reparam
from mitsuba.python.ad.integrators import emission_reparam
from simple import SimpleIntegrator
from simple_flag import SimpleFlagIntegrator
from simple_dfa import SimpleDFAIntegrator
from simple_mis import SimpleMISIntegrator
# from LPE_Engine.drjit_utils import DrJitDFA


def cornell_box_AD():
    '''
    Returns a dictionary containing a description of the Cornell Box scene.
    '''
    T = mi.ScalarTransform4f
    return {
        'type': 'scene',
        'integrator': {
            # 'type': 'simple',
            'type': 'simpleFlag',
            # 'type': 'simpleMIS',
            # 'type': 'emission_reparam',
            # 'type': 'simpleDFA',

            # 'type': 'path',
            # 'max_depth': 2
        },
        # -------------------- Sensor --------------------
        'sensor': {
            'type': 'perspective',
            'fov_axis': 'smaller',
            'near_clip': 0.001,
            'far_clip': 100.0,
            'focus_distance': 1000,
            'fov': 39.3077,
            'to_world': T.look_at(
                origin=[0, 0, 3.90],
                target=[0, 0, 0],
                up=[0, 1, 0]
            ),
            'sampler': {
                'type': 'independent',
                'sample_count': 1024
            },
            'film': {
                'type': 'hdrfilm',
                'width': 256,
                'height': 256,
                'rfilter': {
                    'type': 'gaussian',
                },
                'pixel_format': 'rgb',
                'component_format': 'float32',
            }
        },
        # -------------------- BSDFs --------------------
        'white': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.885809, 0.698859, 0.666422],
            }
        },
        'green': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.105421, 0.37798, 0.076425],
            }
        },
        'red': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.570068, 0.0430135, 0.0443706],
            }
        },
        'large': {
            # m_components.push_back(BSDFFlags::DeltaReflection | BSDFFlags::FrontSide);
            # m_components.push_back(BSDFFlags::DiffuseReflection | BSDFFlags::FrontSide);
            # 'type': 'plastic',
            # "diffuse_reflectance": {
            #     'type': 'rgb',
            #     'value': [0.2, 0.8, 0.12],
            # },

            # BSDFFlags::DeltaReflection | BSDFFlags::FrontSide
            'type': 'conductor',
            'material': 'Au',
        },
        'small': {
            # m_components.push_back(BSDFFlags::GlossyReflection | BSDFFlags::FrontSide);
            # m_components.push_back(BSDFFlags::DiffuseReflection | BSDFFlags::FrontSide);
            'type': 'roughplastic',
            "alpha": 0.1,
            "diffuse_reflectance": {
                'type': 'rgb',
                'value': [0.940, 0.271, 0.361],
            },
        },
        # -------------------- Emitter --------------------
        'emitter': {
                'type': 'constant'
        },
        'light': {
            'type': 'rectangle',
            'to_world': T.translate([0.0, 0.99, 0.01]).rotate([1, 0, 0], 90).scale([0.23, 0.19, 0.19]),
            'bsdf': {
                'type': 'ref',
                'id': 'white'
            },
            'emitter': {
                'type': 'area',
                'radiance': {
                    'type': 'rgb',
                    'value': [18.387, 13.9873, 6.75357],
                    # 'value': [18.387*5, 13.9873*5, 6.75357*5],
                }
            }
        },
        # -------------------- Shapes --------------------
        'floor': {
            'type': 'rectangle',
            'to_world': T.translate([0.0, -1.0, 0.0]).rotate([1, 0, 0], -90),
            'bsdf': {
                'type': 'ref',
                'id':  'white'
            }
        },
        'ceiling': {
            'type': 'rectangle',
            'to_world': T.translate([0.0, 1.0, 0.0]).rotate([1, 0, 0], 90),
            'bsdf': {
                'type': 'ref',
                'id':  'white'
            }
        },
        'back': {
            'type': 'rectangle',
            'to_world': T.translate([0.0, 0.0, -1.0]),
            'bsdf': {
                'type': 'ref',
                'id':  'white'
            }
        },
        'green-wall': {
            'type': 'rectangle',
            'to_world': T.translate([1.0, 0.0, 0.0]).rotate([0, 1, 0], -90),
            'bsdf': {
                'type': 'ref',
                'id':  'green'
            }
        },
        'red-wall': {
            'type': 'rectangle',
            'to_world': T.translate([-1.0, 0.0, 0.0]).rotate([0, 1, 0], 90),
            'bsdf': {
                'type': 'ref',
                'id':  'red'
            }
        },
        'small-box': {
            'type': 'cube',
            'to_world': T.translate([0.335, -0.7, 0.38]).rotate([0, 1, 0], -17).scale(0.3),
            'bsdf': {
                'type': 'ref',
                'id':  'small'
            }
        },
        'large-box': {
            'type': 'cube',
            'to_world': T.translate([-0.33, -0.4, -0.28]).rotate([0, 1, 0], 18.25).scale([0.3, 0.61, 0.3]),
            'bsdf': {
                'type': 'ref',
                'id':  'large'
            }
        },
    }


mi.set_variant('llvm_ad_rgb')
# mi.register_integrator(
#     "direct_reparam", lambda props: DirectReparamIntegrator(props))
mi.register_integrator(
    "simple", lambda props: SimpleIntegrator(props))
mi.register_integrator(
    "simpleFlag", lambda props:  SimpleFlagIntegrator(props))
mi.register_integrator(
    "simpleDFA", lambda props:  SimpleDFAIntegrator(props))
mi.register_integrator(
    "simpleMIS", lambda props:  SimpleMISIntegrator(props))

# regex = "R*T.V?G+S*"
# jitDFA = DrJitDFA(regex)

scene = mi.load_dict(cornell_box_AD())
img = mi.render(scene)


# mi.Bitmap(img).write('flag_G.exr')
mi.Bitmap(img).write('dfa_GE.exr')
# mi.Bitmap(img).write('mis.exr')

