import numpy as np


class Data():
    
    def save(fname, space, waves):
        """Save data and close opened file.Note waves is a list"""
        f = open(fname, 'w')
        header = 'xgrid \t pgrid'
        for wave in waves:
            header = header + ' \t ' + wave.name + '_real' + \
                              ' \t ' + wave.name + '_imag' + \
                              ' \t ' + wave.name + 'hat_real' + \
                              ' \t ' + wave.name + 'hat_imag' + '\n' 
        f.write(header)
        
        data = [space.xgrid.reshape(-1,1), space.pgrid.reshape(-1,1)]
        for wave in waves:
                data += [wave.psi.real.reshape(-1,1), wave.psi.imag.reshape(-1,1),
                        wave.psihat.real.reshape(-1,1), wave.psihat.imag.reshape(-1,1)]
        np.savetxt(f, np.concatenate(data, axis=1), delimiter = '\t')
        f.close()
        
