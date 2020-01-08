# should be run from within the 'testing' directory, otherwise adjust pathnames

from qatoolspython import qatools

qatools.run_qatools(subjects_dir='data', output_dir='output/test11', subjects=['091'])

qatools.run_qatools(subjects_dir='data', output_dir='output/test12', subjects=['129', '130'])

qatools.run_qatools(subjects_dir='data', output_dir='output/test13')

qatools.run_qatools(subjects_dir='data', output_dir='output/test14', screenshots=True)

qatools.run_qatools(subjects_dir='data', output_dir='output/test15', fornix=True)

qatools.run_qatools(subjects_dir='data', output_dir='output/test16', outlier=True)

qatools.run_qatools(subjects_dir='data', output_dir='output/test17', outlier=True, outlier_table='data/buckner_AsegExampleNorms.csv')

qatools.run_qatools(subjects_dir='data', output_dir='output/test18', shape=True, screenshots=True, fornix=True, outlier=True)
