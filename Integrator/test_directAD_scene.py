import drjit as dr
import mitsuba as mi
# from mitsuba.python.ad.integrators.direct_reparam import DirectReparamIntegrator
from mitsuba.python.ad.integrators import direct_reparam
from mitsuba.python.ad.integrators import emission_reparam
from direct import DirectIntegrator
from direct_flag import DirectFlagIntegrator
from direct_dfa import DirectDFAIntegrator
from direct_mis import DirectMISIntegrator
from  path_mis import PathMisIntegrator
from  path_mats_dfa import PathMatsDFAIntegrator
from  path_mats import PathMatsIntegrator
from  path_mis_dfa import PathMisDFAIntegrator
# from LPE_Engine.drjit_utils import DrJitDFA


def cornell_box_AD():
    '''
    Returns a dictionary containing a description of the Cornell Box scene.
    '''
    T = mi.ScalarTransform4f
    return {
        'type': 'scene',
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
                'sample_count': 256
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
            # 'type': 'conductor',
            # 'material': 'Au',


            # BSDFFlags::DeltaReflection | BSDFFlags::FrontSide
            # BSDFFlags::DeltaTransmission | BSDFFlags::FrontSide
            'type':"dielectric",
            "int_ior":"diamond",
            "ext_ior":"air",
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
    "direct", lambda props: DirectIntegrator(props))
mi.register_integrator(
    "directFlag", lambda props:  DirectFlagIntegrator(props))
mi.register_integrator(
    "directDFA", lambda props:  DirectDFAIntegrator(props))
mi.register_integrator(
    "directMIS", lambda props:  DirectMISIntegrator(props))
mi.register_integrator(
    "pmis", lambda props:  PathMisIntegrator(props))
mi.register_integrator(
    "pmatsDFA", lambda props:  PathMatsDFAIntegrator(props))

mi.register_integrator(
    "pmats", lambda props:  PathMatsIntegrator(props))

mi.register_integrator(
    "pmisDFA", lambda props:  PathMisDFAIntegrator(props))


scene = mi.load_dict(cornell_box_AD())

inegrator1 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'DRE',
        'max_depth': 10,
    })
img1 = mi.render(scene, integrator=inegrator1)

inegrator2 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'DR.+E',
        'max_depth':10,
    })
img2 = mi.render(scene, integrator=inegrator2)

inegrator3 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'DT.*E',
        'max_depth': 10,
    })
img3 = mi.render(scene, integrator=inegrator3)

inegrator4 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'SRE',
        'max_depth': 10,
        
    })
img4 = mi.render(scene, integrator=inegrator4)

inegrator5 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'SR.+E',
        'max_depth': 10,
    })
img5 = mi.render(scene, integrator=inegrator5)

inegrator6 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'ST.*E',
        'max_depth': 10,
        
    })
img6 = mi.render(scene, integrator=inegrator6)

inegrator7 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'E',
        'max_depth': 10,
    })
img7 = mi.render(scene, integrator=inegrator7)

inegrator8 = mi.load_dict(
    {
        'type': 'pmisDFA',
        'lpe':'G.*E',
        'max_depth': 10,
        
    })
img8 = mi.render(scene, integrator=inegrator8)

# inegrator9 = mi.load_dict(
#     {
#         'type': 'pmisDFA',
#         'lpe': 'A+D*E',
#         'max_depth': 10,
#     })
# img9 = mi.render(scene, integrator=inegrator9)

inegrator10 = mi.load_dict(
    {
        'type': 'path',
        # 'lpe': 'A*G*E',
        'max_depth': 10,
    })
img10 = mi.render(scene, integrator=inegrator10)



mi.Bitmap(img1).write('5_mis_directDiffuse.exr')
mi.Bitmap(img2).write('5_mis_indirectDiffuse.exr')
mi.Bitmap(img3).write('5_mis_subsurface.exr')
mi.Bitmap(img4).write('5_mis_directSpecular.exr')
mi.Bitmap(img5).write('5_mis_directSpecular.exr')
mi.Bitmap(img6).write('5_mis_transmissive.exr')
mi.Bitmap(img7).write('5_mis_emissive.exr')
mi.Bitmap(img8).write('5_mis_glossy.exr')
mi.Bitmap(img1+img2+img3+img4+img5+img6+img7+img8).write('5_mis_all.exr')
mi.Bitmap(img10).write('path_10.exr')





# mi.Bitmap(img1).write('validation_report/mis2.exr')
# mi.Bitmap(img2).write('validation_report/mis6.exr')
# mi.Bitmap(img3).write('validation_report/mis10.exr')
# mi.Bitmap(img4).write('validation_report/mis_DE.exr')
# mi.Bitmap(img5).write('validation_report/mis_AE.exr')
# mi.Bitmap(img6).write('validation_report/mis_GE.exr')
# mi.Bitmap(img7).write('validation_report/mis_E.exr')
# mi.Bitmap(img8).write('validation_report/mis_D+E10.exr')
# mi.Bitmap(img9).write('validation_report/mis_A+D*E10.exr')
# mi.Bitmap(img10).write('validation_report/mis_A*G*E10.exr')

# mi.Bitmap(img4+img5+img6+img7).write('validation_report/mis_all.exr')
# mi.Bitmap(img4+img6+img8+img10).write('validation_report/flag_all.exr')

# mi.Bitmap(img1).write('try_pmis_DE2.exr')
# mi.Bitmap(img1 - img2).write('try_diff_D*E.exr')
# mi.Bitmap(img2 - img1).write('try_diff_D*E2.exr')
# mi.Bitmap(img3).write('try_pmats_notDE.exr')
# mi.Bitmap(img4).write('ref_direct_emitter.exr')
# mi.Bitmap(img2).write('pmis_lobe_6.exr')



