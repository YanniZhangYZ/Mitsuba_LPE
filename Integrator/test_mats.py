import drjit as dr
import mitsuba as mi
from  path_mats_LPE import PathMatsLPEIntegrator
from  path_mats import PathMatsIntegrator


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

mi.register_integrator(
    "pmatsLPE", lambda props:  PathMatsLPEIntegrator(props))

mi.register_integrator(
    "pmats", lambda props:  PathMatsIntegrator(props))

scene = mi.load_dict(cornell_box_AD())


inegrator1 = mi.load_dict(
    {
        'type': 'path',
        'max_depth': 10,
    })
img1 = mi.render(scene, integrator=inegrator1)
name = 'path_10'
mi.Bitmap(img1).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img1)


inegrator2 = mi.load_dict(
    {
        'type': 'pmats',
        'max_depth': 10,
    })
img2 = mi.render(scene, integrator=inegrator2)
name = '1_mats'
mi.Bitmap(img2).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img2)


inegrator3 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'D.E',
        'max_depth': 2,
    })
img3 = mi.render(scene, integrator=inegrator3)
name = '1_mats2_D.E'
mi.Bitmap(img3).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img3)


inegrator4 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'G.E',
        'max_depth': 2,
    })
img4 = mi.render(scene, integrator=inegrator4)
name = '1_mats2_G.E'
mi.Bitmap(img4).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img4)


inegrator5 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'S.E',
        'max_depth': 2,
    })
img5 = mi.render(scene, integrator=inegrator5)
name = '1_mats2_S.E'
mi.Bitmap(img5).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img5)


inegrator6 = mi.load_dict(
    {
       'type': 'pmatsLPE',
        'lpe':'E',     
        'max_depth': 2,
    })
img6 = mi.render(scene, integrator=inegrator6)
name = '1_mats2_E'
mi.Bitmap(img6).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img6)


name = '1_mats2_all'
mi.Bitmap(img3+img4+img5+img6).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img3+img4+img5+img6)


# =============================================================
#       mats 10
# =============================================================


inegrator7 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'D.*E',     
        'max_depth': 10,
    })
img7 = mi.render(scene, integrator=inegrator7)
name = '1_mats_D'
mi.Bitmap(img7).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img7)


inegrator8 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'S.*E',     
        'max_depth': 10,
    })
img8 = mi.render(scene, integrator=inegrator8)
name = '1_mats_S'
mi.Bitmap(img8).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img8)


inegrator9 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'G.*E',     
        'max_depth': 10,
    })
img9 = mi.render(scene, integrator=inegrator9)
name = '1_mats_G'
mi.Bitmap(img9).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img9)


inegrator10 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'E',     
        'max_depth': 10,
    })
img10 = mi.render(scene, integrator=inegrator10)
name = '1_mats_E'
mi.Bitmap(img10).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img10)



name = '1_mats_all'
mi.Bitmap(img7+img8+img9+img10).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img7+img8+img9+img10)


# =============================================================
#       complement
# =============================================================


inegrator11 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'D.*E',     
        'max_depth': 10,
        'complement':True,
    })
img11 = mi.render(scene, integrator=inegrator11)
name = '1_C_mats_D.*E'
mi.Bitmap(img11).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img11)

name = '1_C_mats_D.*E_all'
mi.Bitmap(img11+img7).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img11+img7)


inegrator12 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'G.*E',     
        'max_depth': 10,
        'complement':True,
    })
img12 = mi.render(scene, integrator=inegrator12)
name = '1_C_mats_G.*E'
mi.Bitmap(img12).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img12)

name = '1_C_mats_G.*E_all'
mi.Bitmap(img12+img9).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img12+img9)


inegrator13 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'S.*E',     
        'max_depth': 10,
        'complement':True,
    })
img13 = mi.render(scene, integrator=inegrator13)
name = '1_C_mats_S.*E'
mi.Bitmap(img13).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img13)

name = '1_C_mats_S.*E_all'
mi.Bitmap(img13+img8).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img13+img8)


inegrator14 = mi.load_dict(
    {
       'type': 'pmatsLPE',
        'lpe':'E',     
        'max_depth': 10,
        'complement':True,  
    })
img14 = mi.render(scene, integrator=inegrator14)
name = '1_C_mats_E'
mi.Bitmap(img14).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img14)


name = '1_C_mats_E_all'
mi.Bitmap(img14+img10).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img14+img10)





# =============================================================
#  complex complement
# =============================================================

inegrator15 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'D.S.*E',
        'complement':True,
        'max_depth': 10,
    })
img15 = mi.render(scene, integrator=inegrator15)
name = '1_C_mats_D.S.*E'
mi.Bitmap(img15).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img15)


inegrator16 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'D.S.*E',
        # 'complement':True,
        'max_depth': 10,
        
    })
img16 = mi.render(scene, integrator=inegrator16)
name = '1_mats_D.S.*E'
mi.Bitmap(img16).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img16)

name = '1_C_mats_D.S.*E_all'
mi.Bitmap(img16+img15).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img16+img15)



inegrator17 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'G.D.*E',
        'complement':True,
        'max_depth': 10,
    })
img17 = mi.render(scene, integrator=inegrator17)
name = '1_C_mats_G.D.*E'
mi.Bitmap(img17).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png',img17)


inegrator18 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'G.D.*E',
        # 'complement':True,
        'max_depth': 10,
    })
img18 = mi.render(scene, integrator=inegrator18)
name = '1_mats_G.D.*E'
mi.Bitmap(img18).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img18)

name = '1_C_mats_G.D.*E_all'
mi.Bitmap(img18+img17).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img18+img17)



inegrator19 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'S.D.*E',
        'complement':True,
        'max_depth': 10,
    })
img19 = mi.render(scene, integrator=inegrator19)
name = '1_C_mats_S.D.*E'
mi.Bitmap(img19).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png',img19)


inegrator20 = mi.load_dict(
    {
        'type': 'pmatsLPE',
        'lpe':'S.D.*E',
        # 'complement':True,
        'max_depth': 10,
    })
img20 = mi.render(scene, integrator=inegrator20)
name = '1_mats_S.D.*E'
mi.Bitmap(img20).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img20)

name = '1_C_mats_S.D.*E_all'
mi.Bitmap(img20+img19).write(name+'.exr')
mi.util.write_bitmap('report/'+name+'.png', img20+img19)



