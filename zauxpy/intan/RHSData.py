#!/usr/bin/env python

import pathlib


ZAUX_MODULE_RHSDATA_IMPORTED = True

class RHSData:

    def load(self):

        print(">>> ")
        self.data = read_data(str(self.rhs_path), verbose=False)
        self.is_loaded = True
        for key, value in self.data.items():
            assert not hasattr(self, key)
            setattr(self, key, value)

        self.stim_chan_name = "B-014"
        self.plot_chan_names = [f"B-{i:03d}" for i in range(10, 19)]
        self.stim_chan_idx = self.chan_names.index(self.stim_chan_name)
        self.plot_chan_idxs = [self.chan_names.index(n) for n in self.plot_chan_names]

        self.t_stim_i = self.data['t'][self.data['stim_data'][self.stim_chan_idx, :] != 0][0]
        self.ts_stim_i = list(self.data['t']).index(self.t_stim_i)

    def __init__(self, rhs_path, do_load=False):

        if isinstance(rhs_path, str):
            rhs_path = pathlib.Path(rhs_path)
        assert rhs_path.is_file()
        self.rhs_path = rhs_path
        self.is_loaded = False
        self.simple_traces_plot = None
        self.stim_chan_name = "B-014"
        self.plot_chan_names = [f"B-{i:03d}" for i in range(10, 19)]
        if do_load:
            self.load()

    def __repr__(self):

        _multiline_repr = True
        if _multiline_repr:
            _repr_temp = "{}(\n\t{}\n)"
            _repr_join = ",\n\t"
            _repr_attr_fmt = "{} = {}"
        else:
            _repr_temp = "{}({})"
            _repr_join = ", "
            _repr_attr_fmt = "{}={}"

        _excl_attrs = ['data']
        if self.is_loaded:
            _excl_attrs = [*_excl_attrs, *self.data.keys()]
        _repr_attrs = [
            attr for attr in self.__dict__.keys()
                if not attr.startswith('_') and
                    attr not in _excl_attrs
        ]

        self._repr = _repr_temp.format(
            self.__class__.__name__,
            _repr_join.join([
                _repr_attr_fmt.format(attr, repr(getattr(self, attr)))
                for attr in _repr_attrs
            ])
        )
        return self._repr

    @property
    def chan_names(self):
        assert self.is_loaded
        self._chan_names = [c['native_channel_name'] for c in self.amplifier_channels]
        return self._chan_names

    def plot_simple_traces(self,
                           stim_chan_name,
                           plot_chan_names,
                           do_save=False,
                           plot_root=pathlib.Path.cwd(),
                           plot_stem="simple_traces",
                           # plot_stem_temp="{0.rhs_path.parent.name}.{0.trial_idx:03d}.simple_traces",
                           plot_ext='png',
                           plot_suptitle=None,
                           plot_size=(50, 30),
                           do_zoom=True):

        assert self.is_loaded

        stim_chan_idx = self.chan_names.index(stim_chan_name)
        plot_chan_idxs = [self.chan_names.index(n) for n in plot_chan_names]

        nsr, nsc = len(plot_chan_idxs) + 1, 1
        fig, ax = plt.subplots(nsr, nsc, sharex=True, figsize=plot_size, constrained_layout=True)
        for sp in range(nsr):
            if sp < (nsr - 1):
                ax[sp].plot(self.t, self.amplifier_data[plot_chan_idxs[sp], :])
                ax[sp].set_ylabel("LFP ($\mu$V)")
                ax[sp].set_title(plot_chan_names[sp])
            else:
                ax[sp].plot(self.t, self.stim_data[stim_chan_idx, :])
                ax[sp].set_title(f"Stimulation ({stim_chan_name})")
                ax[sp].set_ylabel("Stim ($\mu$V)")
            # if plot_chan_names[sp] == stim_chan_name:
            #     ax[sp].plot(trial.t, trial.stim_data[plot_chan_idxs[sp], :])
        # sp += 1
        # fig.add_subplot(nsr, nsc, sp)
        # plt.plot(trial.t, trial.stim_data[stim_chan_idx, :])
        # plt.set_ylabel("Stim ($\mu$V)")
        ax[sp].set_xlabel("time (sec)")
        # fig.show()

        if True:
            ax[4].set_title("B-014 [stim]", fontweight='bold', color=(0.8, 0, 0))
            ax[7].set_title("B-017 [rec]", fontweight='bold', color=(0, 0.5, 0))
            ax[9].set_title("Stimulation (B-014)", fontstyle='italic', color=(0.6, 0, 0))
            # plt.xlim(trial.t_stim_i - 0.005, trial.t_stim_i + 0.01)

        for ax_i in range(len(ax)):
            ax[ax_i].minorticks_on()
            ax[ax_i].grid(which='major')
            ax[ax_i].grid(which='minor')

        if plot_suptitle is not None:
            fig.suptitle(plot_suptitle, fontsize=16)

        if do_save:

            if not isinstance(plot_root, pathlib.Path):
                plot_root = pathlib.Path(plot_root)
            assert plot_root.is_dir()

            # plot_stem = plot_stem_temp.format(self)
            plot_path = plot_root / f"{plot_stem}.{plot_ext}"
            _, t = msg(f"saving plot to ``{plot_path}...")
            fig.savefig(plot_path)
            msg(f"saved plot in {localnow() - t}")

            # plot_pkl = plot_path.with_suffix('.pkl')
            # _, t = msg(f"pickling plot to ``{plot_pkl}...")
            # with plot_pkl.open('wb') as fid:
            #     pickle.dump([fig, ax], fid)
            # msg(f"pickled plot in {localnow() - t}")

            self.simple_traces_plot_path = plot_path
            # self.simple_traces_plot_pkl = plot_pkl

        if do_zoom:
            # plt.xlim(self.t_stim_i - 0.05, self.t_stim_i + 0.1)
            plt.xlim(self.t_stim_i - 0.005, self.t_stim_i + 0.01)

            if do_save:
                plot_path = plot_path.parent / f"{plot_path.stem}_zoom.{plot_ext}"
                _, t = msg(f"saving zoomed plot to ``{plot_path}...")
                fig.savefig(plot_path)
                msg(f"saved plot in {localnow() - t}")

        self.simple_traces_plot = [fig, ax]

        return self.simple_traces_plot
