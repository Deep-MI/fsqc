# should be run from within the 'testing' directory, otherwise adjust pathnames

../qatools --subjects_dir data --output_dir output/test01 --subjects 091

../qatools --subjects_dir data --output_dir output/test02 --subjects 129 130

../qatools --subjects_dir data --output_dir output/test03

../qatools --subjects_dir data --output_dir output/test04 --screenshots

../qatools --subjects_dir data --output_dir output/test05 --fornix

../qatools --subjects_dir data --output_dir output/test06 --outlier

../qatools --subjects_dir data --output_dir output/test07 --outlier --outlier-table data/buckner_AsegExampleNorms.csv

../qatools --subjects_dir data --output_dir output/test08 --screenshots --fornix --outlier

