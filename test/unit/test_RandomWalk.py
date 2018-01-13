import porespy as ps
import pytrax as pt
import scipy as sp
import os
import matplotlib.pyplot as plt


class SimulationTest():
    def setup_class(self):
        self.l = 100
        self.im = ps.generators.overlapping_spheres(shape=[self.l, self.l],
                                                    radius=5,
                                                    porosity=0.55)
        self.blobs = ps.generators.blobs([self.l, self.l, self.l])
        self.rw = pt.RandomWalk(self.blobs)
        self.blobs_2d = ps.generators.blobs([self.l, self.l]).astype(int)
        self.rw_2d = pt.RandomWalk(self.blobs_2d, seed=True)

    def test_random_walk(self):
        self.rw.run(nt=1000, nw=100, stride=1)
        assert sp.shape(self.rw.real_coords) == (1000, 100, 3)

    def test_plot_msd(self):
        self.rw.plot_msd()
        pass

    def test_random_walk_2d(self):
        self.rw_2d.run(nt=1000, nw=100, same_start=True, stride=100)
        assert sp.shape(self.rw_2d.real_coords) == (10, 100, 2)

    def test_plot_walk_2d(self):
        self.rw_2d.plot_walk_2d(data='w')
        assert hasattr(self.rw_2d, 'im_big')
        assert sp.sum(self.rw_2d.im_big > self.rw_2d.nw) == 0
        plt.close('all')

#    def test_export(self):
#        cwd = os.getcwd()
#        self.rw_2d.export_walk(sub='temp', image=self.rw_2d.im, sample=10)
#        subdir = os.path.join(cwd, 'temp')
#        assert os.path.exists(subdir)
#        file_list = os.listdir(subdir)
#        # 10 coordinate files based on the stride and number of steps + image
#        assert len(file_list) == 11
#        # Delete all files and folder
#        for file in file_list:
#            fp = os.path.join(subdir, file)
#            os.remove(fp)
#        os.rmdir(subdir)

    def test_seed(self):
        # rw_2d was initialized with seed = True, this should mean running it
        # repeatedly produces the same movements
        self.rw_2d.run(nt=1000, nw=100, same_start=True)
        temp_coords = self.rw_2d.real_coords.copy()
        self.rw_2d.run(nt=1000, nw=100, same_start=True)
        assert sp.allclose(self.rw_2d.real_coords, temp_coords)

    def test_axial_density_plot(self):
        self.rw.axial_density_plot(time=0, axis=0)
        plt.close('all')

    def test_rw_analytics(self):
        w_list = [100]
        t_list = [100]
        self.rw_2d.run_analytics(w_list, t_list, fname='test.csv', num_proc=1)
        cwd = os.getcwd()
        fpath = os.path.join(cwd, 'test.csv')
        assert os.path.exists(fpath)
        os.remove(fpath)
        plt.close('all')

if __name__ == '__main__':
    t = SimulationTest()
    t.setup_class()
    t.test_random_walk()
    t.test_plot_msd()
    t.test_random_walk_2d()
    t.test_plot_walk_2d()
#    t.test_export()
    t.test_seed()
    t.test_axial_density_plot()
    t.test_rw_analytics()
