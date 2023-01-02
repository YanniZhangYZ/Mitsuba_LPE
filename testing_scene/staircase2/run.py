import drjit as dr
import mitsuba as mi
from  Integrator.path_mis_LPE import PathMisLPEIntegrator
from Integrator.path_mis import PathMisIntegrator

mi.set_variant('llvm_ad_rgb')
mi.register_integrator(
    "pmisLPE", lambda props:  PathMisLPEIntegrator(props))

mi.register_integrator(
    "pmis", lambda props:  PathMisIntegrator(props))

scene = mi.load_file("testing_scene/staircase2/scene.xml")

# inegrator0 = mi.load_dict(
#     {
#         'type': 'pmis',
#         'max_depth': 65,
#     })
# img0 = mi.render(scene, integrator=inegrator0)
# name = 'testing_scene/staircase2/origin'
# mi.Bitmap(img0).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img0)

# inegrator1 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'E',     
#         'max_depth': 65,
#     })
# img1 = mi.render(scene, integrator=inegrator1)
# name = 'testing_scene/staircase2/emissive'
# mi.Bitmap(img1).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img1)

inegrator2 = mi.load_dict(
    {
        'type': 'pmisLPE',
        'lpe':'DRE',     
        'max_depth': 65,
    })
img2 = mi.render(scene, integrator=inegrator2)
name = 'testing_scene/staircase2/directDiffuse'
mi.Bitmap(img2).write(name+'.exr')
mi.util.write_bitmap(name+'.png', img2)

# inegrator3 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'DR.+E',     
#         'max_depth': 65,
#     })
# img3 = mi.render(scene, integrator=inegrator3)
# name = 'testing_scene/staircase2/indirectDiffuse'
# mi.Bitmap(img3).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img3)

# inegrator4 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'GR.*E',     
#         'max_depth': 65,
#     })
# img4 = mi.render(scene, integrator=inegrator4)
# name = 'testing_scene/staircase2/glossy'
# mi.Bitmap(img4).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img4)


# inegrator5 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'SRE',     
#         'max_depth': 65,
#     })
# img5 = mi.render(scene, integrator=inegrator5)
# name = 'testing_scene/staircase2/directSpecular'
# mi.Bitmap(img5).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img5)

# inegrator6 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'SR.+E',     
#         'max_depth': 65,
#     })
# img6 = mi.render(scene, integrator=inegrator6)
# name = 'testing_scene/staircase2/indirectSpecular'
# mi.Bitmap(img6).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img6)

# inegrator7 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'ST.*E',     
#         'max_depth': 65,
#     })
# img7 = mi.render(scene, integrator=inegrator7)
# name = 'testing_scene/staircase2/transmissive'
# mi.Bitmap(img7).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img7)

# inegrator8 = mi.load_dict(
#     {
#         'type': 'pmisLPE',
#         'lpe':'ST.*E',   
#         'complement': True, 
#         'max_depth': 65,
#     })
# img8 = mi.render(scene, integrator=inegrator8)
# name = 'testing_scene/staircase2/transmissive_comp'
# mi.Bitmap(img8).write(name+'.exr')
# mi.util.write_bitmap(name+'.png', img8)