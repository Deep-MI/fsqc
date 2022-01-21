# should be run from within the 'testing' directory, otherwise adjust pathnames; check which version is executed, i.e. an installed old one, or the modified local one?

from qatoolspython import qatoolspython

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test101', subjects=['091'])

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test102', subjects=['129', '130'])

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test103')

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test104', screenshots=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test105', fornix=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test106', outlier=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test107', outlier=True, outlier_table='data/buckner_AsegExampleNorms.csv')

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test108', screenshots=True, fornix=True, outlier=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test109', subjects=['129', '130'], screenshots=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test110', subjects=['129', '130'], screenshots=True, screenshots_views=['x=10', 'x=-10', 'y=0', 'z=0'])

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test111', subjects=['129', '130'], screenshots=True, screenshots_views=['z=10', 'y=-5'], screenshots_html=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test112', subjects=['129'], screenshots=True, screenshots_base='data/129/mri/orig.mgz', screenshots_overlay='none')

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test113', subjects=['129'], screenshots=True, screenshots_overlay='data/129/mri/aparc+aseg.mgz')

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test114', subjects=['129'], screenshots=True, screenshots_overlay='none', screenshots_surf=['data/129/surf/lh.white'])

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test115', subjects=['129'], screenshots=True, screenshots_overlay='none', screenshots_surf=['data/129/surf/rh.white', 'data/129/surf/lh.pial'])

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test116', screenshots=True, fornix=True, outlier=True, fornix_html=True, shape=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test117', subjects_file='subjects.lst')

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test118', subjects=['129', '130'], screenshots=True, screenshots_views=['z=10', 'y=-5'], screenshots_layout=['2', '1'])

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test119', subjects=['129', '130'], screenshots=True, screenshots_views=['z=10', 'y=-5', 'z=-10', 'y=5', 'x=0'], screenshots_layout=['1', '5'], screenshots_html=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test120', fornix=True, fornix_html=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test121', subjects=['129', '130'], screenshots=True, screenshots_base='orig.mgz', screenshots_overlay=None, screenshots_html=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test122', subjects=['129', '130'], screenshots=True, screenshots_base='orig.mgz', screenshots_overlay='aparc+aseg.mgz', screenshots_html=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test123', subjects=['129', '130'], screenshots=True, screenshots_overlay='none', screenshots_surf="lh.white", screenshots_html=True) # note 'none' vs. None (in test121)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test124', subjects=['129', '130'], screenshots=True, screenshots_base='orig.mgz', screenshots_surf=["lh.pial", "rh.white"], screenshots_html=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test125', hypothalamus=True)

qatoolspython.run_qatools(subjects_dir='data', output_dir='output/test126', hypothalamus=True, hypothalamus_html=True, fornix=True, fornix_html=True, screenshots=True, screenshots_html=True)

