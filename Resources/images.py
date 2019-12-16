"""
Copyright 2019 iACT, Universite de Montreal,
Jean Piche, Olivier Belanger, Jean-Michel Dumas

This file is part of Cecilia 5.

Cecilia 5 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cecilia 5 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cecilia 5.  If not, see <http://www.gnu.org/licenses/>.
"""

from wx.lib.embeddedimage import PyEmbeddedImage

# ***************** Catalog starts here *******************

catalog = {}
index = []

#----------------------------------------------------------------------
arrow_down_hover = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAKCAYAAACJxx+AAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAANrAAADawB7wbGRwAAAI1JREFUGJVt0LFqQlEQhOFvw32CkMbeWPoMBgRfUssU6fMi'
    b'WhhCmlQptLA11VjkXDloFhaWmX+WZQsrfCf51FVVzTAdcMK+qnb4av4z5lhIAlvkpj+SeGiJ'
    b'jftaw7jhEecu/YunJH9Ag1474O2qd8BLByz/AwoHHFGjPowXJUlVvTcz1390s6qaNO1n1C6G'
    b'EFt0TbKPGQAAAABJRU5ErkJggg==')
index.append('arrow_down_hover')
catalog['arrow_down_hover'] = arrow_down_hover

#----------------------------------------------------------------------
arrow_down = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAKCAYAAACJxx+AAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAANrAAADawB7wbGRwAAANpJREFUGJVdjLFqg1AYhY+mKb24uPgUvkAHXySDiHsHpy61'
    b'D9CpOHXRQAbfwUkaBLkogoIZs7WCg53bNO3p0iuSb/r5zvmP5nnes2maxyiKXkj+4B/XdTck'
    b'bzXf9+/jOH4qy/I0DMOHEGIthDAcx7kJguARALQsyz55QZ7nXwB0nSSllK+4QEq5J/mrA0BV'
    b'VeE4jnM4TRO6rnsAAJAESSRJ8qbm0zR9V15XX03TbBf3bp5TTQDroijOdV2fbdu+Vv5qUfwO'
    b'w/BgGIbW9/1J+bkAAG3b3lmWtVq6Pyhsir01ukkfAAAAAElFTkSuQmCC')
index.append('arrow_down')
catalog['arrow_down'] = arrow_down

#----------------------------------------------------------------------
arrow_up_hover = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAKCAYAAACJxx+AAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAANrAAADawB7wbGRwAAAINJREFUGJV1zaEOQQEUBuDv2BUEm2ATCcwUTTPdMwieS7Sp'
    b'3kXFA2iioBzBxb3Gv/3l7DvnyEyvoo9ubfYFdtj8BGjgiss/sESWnf8C+wrY1gB6uFfADZ3M'
    b'1PDMGk2ftLDC+8Kxsv3qITMVEbHAEAecywsjTCNiVqCNSWaeKi9ExBiDBzGacT4RANd0AAAA'
    b'AElFTkSuQmCC')
index.append('arrow_up_hover')
catalog['arrow_up_hover'] = arrow_up_hover

#----------------------------------------------------------------------
arrow_up = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAKCAYAAACJxx+AAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAANrAAADawB7wbGRwAAANlJREFUGJVlkKFuhEAYhGcLprIGe8iKlqRyKZIgeAMaDJcN'
    b'D1DfpPJeoB5XiV8M5iwOjSIpCakgubQJ6U5N2Vx6n5pM/v8TI0hiI0mSRwDQWh+3zsUZQRC8'
    b'GWMI4OHiQAjhNE1zt64rhBAOyR8AAEmQhFLqlSSNMczz/GXrrzaDlHL/Z7LZGtI0vZ+miRvD'
    b'MFBKeWsNYRgePM+zT77vI4qigzW0bfvNf9R1fSIJZ57n57IsU631V9d1n33fn8ZxdOM4vs6y'
    b'7MNdluVGKfVUVdX7+SZFUexJ7n4BAlmFA6WrLtoAAAAASUVORK5CYII=')
index.append('arrow_up')
catalog['arrow_up'] = arrow_up

#----------------------------------------------------------------------
audio_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAc5JREFUWIXt1j1oFUEcBPDfS6IIilUKESTs2ogICokRJKJC'
    b'kPMDCwvFzkYshaA2goJWEhAE26hYRGytFrGwtLFQOw132lhEqwh+EROLnBDExLd5FxSSgYPj'
    b'vzdzw3A7t63Z2Vn/M7r+tYG/YdVgp1g12ClWnsEU4oMUYmPd1dOUUAqxDzew97f5ZjzBF+wp'
    b'qnI6R7eRBFOIu3EVp7Bl/lpRle9xBs/wMoV4MEc7K8EU4roFOFdwbAHOSFGVN1OIk9iJEynE'
    b'vqIq7zVqMIXYjQvY/4flwUWooynEKdwvqnIohfgQd9GsQazFIezL4MBhnMd2jGAqh5zzDfZg'
    b'Mkcciqp8jG04Wo8+5/BzEpzBUutjCp/q++4cYo7BVn0tBeuxpr6fySHm9mB2b9ab4ike1aPe'
    b'5XrhD2zIEa9xAMNFVb6qO/C7uU5sCzkGv+G2uTR68BXT2ISz2LgAb0dRlR9SiCcxjsvm6qot'
    b'tJo48qcQr+M0tv6aFVXZmrd+EUN4jvGiKifa1e74V5dC7MIobi3y2CXsGhvov3bk3duJVqv9'
    b'vdZIgpBC7MVxnMPg/AQ7QWPHrbGB/o/Db17fwYumNGkwweXCyjtRN41Vg51i1WCn+AlFl3Lb'
    b'+CmHgwAAAABJRU5ErkJggg==')
index.append('audio-click-trans')
catalog['audio-click-trans'] = audio_click_trans

#----------------------------------------------------------------------
audio_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAdNJREFUWIXt1j1oFUEUBeDvJVEExSqICJLCYkQk2qggURSC'
    b'rD9YWCh2FoqlQ1AbQUEricgqtlGriJVgNYiFpY2FisVi2qSIVhH8IyYWeUIQE9/kbVDIOzAw'
    b'3Nlz5nDYvXsbs7Oz/md0/WsDf0PHYLvoGGwXK89giOlRiKm23tVTl1CIqQ83sfe3+iY8xxfs'
    b'qcpiOke3lgRDTLtwDaewef5ZVRYTOIOXeBNiOpijnZVgiGnNApyrOLYAZ6gqi9shpknswIkQ'
    b'U19VFg9bubPlBENM3biIJ39Y+xehDoeYzmKiKosBbMCDVu/NSXA1DmFfBgcO4wK2YQhTOeSc'
    b'd7AHkzniUJXFM2zF0Wbpcw4/J8EZLLV9TOFTc9+dQ8wx2GiupWAtVjX3MznE3D6Y3TdDTI/x'
    b'Ak+bpd7luvAH1uWIN3EAg1VZvG32wO/memJLyDH4DffMpdGDr5jGRpzD+gV426uy+BBiOolR'
    b'XDHXrlpCo46RP8R0A6ex5VetKovGvPNLGMArjFZlMdaqdtu/uhBTF4ZxZ5HHLmNn//jI9fd3'
    b'j4w1Gq1/a7UkCCGmXhzHeeyen2A7qG3c6h8f+fju1uB9vK5LkxoTXC6svIm6bnQMtouOwXbx'
    b'E0PNduXRvLOYAAAAAElFTkSuQmCC')
index.append('audio-hover-trans')
catalog['audio-hover-trans'] = audio_hover_trans

#----------------------------------------------------------------------
audio_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAaFJREFUWIXt1j9rVEEUhvHf3UQRDKkUxEbBRsTWNCoaEEGE'
    b'VFnBzkasRAhYiKUfQSxNYRG11c7KwsImhQipbGxNqggisslrca+QxHXdyd6gkH1guPOHc+a9'
    b'w5lzpkrif6bzrwX8jbHAURkLHJV9KfA5WstdbQo8gRc4v2P+OFawjMlir0naaOeSLGY7W9dn'
    b'kjxJspJktsR3qZBDSab6tNf5nV82C833ZJJ3SR4nuTXsnlVBqZvAA1zqszaD6R1zVfPdwB08'
    b'ww+8xI0t6wMpiYmDuIqLBTZwDfdwBgtYLzEuuSST+FLivOENTuN6M/5WYlxygpt2nz7W8bXp'
    b'T5QYlgisDBk3fTiMA01/s8SwNC+V57H6UrzFq2Z8ZK823MBUifOGy7iCj5hV3+T3wxqXpJkO'
    b'5nBW/WPf0cMx3PbnNHMUq+rUsoSHeIq1tgUO4hFu4lQfgXAfF9TlbgmfhvbcQpnrJJlOcndA'
    b'qVtN8nl+fl5VVUX7tnWC1ME/p64aM3Z/47fR2mum2+2u9Xq9RXxoyyftxeCesS9f1K0yFjgq'
    b'Y4Gj8hMzObAudOMxgQAAAABJRU5ErkJggg==')
index.append('audio-normal-trans')
catalog['audio-normal-trans'] = audio_normal_trans

#----------------------------------------------------------------------
Cecilia_about_small = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAEYAAABGCAYAAABxLuKEAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAE6lJREFUeJztXHdwXMd5/+3ua/eu49BBEoUg2KtskjIpWxQd'
    b'ObQilzElxw4tF9l/OG4TpUwmE3smdWI7HhfZVhwVS5Y9zjhudEjLjbZkkWJRYYPYQJDo7YA7'
    b'XH/3ym7+eAfwQALE3QG0lJl8M/gDr+y3+3tf32+PCCHw/3QjSa8R31A+byzJpNOrJhOJJULw'
    b'CEA0ABQQthDIaaoa9QcC3V6vt1uS5CEAmT/kBP9QwIRHR4bvvHL1ynt6evt2DI1E6yeTGTWb'
    b'y5O85QCUgRIGEABCgDsOGAUUmcLn1XhVKGA01ddebm1tea6tte3HwVD4GADjVk6Y3EJVkgYG'
    b'+u9/6aWXHuzq7tk2NBb35m0Cpvogqx5IsgJKGQghILO8LAAIzuFwB7aVh2Vkwa0svBoTzU21'
    b'k2tXdzyzZcttjwSDoSOFxxeVFh0YwfmyV891PvT8kaN7z3f1NdpEIx5fGIrqAaEEEALl8yQg'
    b'xIWPc458LgMjE4Nfg7N+Vfv5O+7Y8WRLS9t/YBHVbTGBCZ0+dfIff3nodx+5OjjhVb3V8HgD'
    b'IIRACL5YPFwiBAQEjuMgk4qBmAlsXtc+9Na77vrSsuaWhwFYC2axGMAMDQ782U/2/+wLnV0D'
    b'jVqgHh7dB6ASySifCKEQQiCdnADycbFz68bj99xzzyd9Pv/LCxp3IZPnnLf+/vfPfuFnzxx6'
    b't8VCzB+MQEAAr0EIQAgFFxyJ8SHUBmjmvne/41vr1m/4JwCTFY1XKTCpVPLup7/7vSdPX+xv'
    b'CNa2QGLS4qtMBUQog5HLwJgcwNt37zi+Z8+e9zMmXSl7nAqAIcNDgw88+u2nvjGWIt5AuO51'
    b'AUgxuXZNID7WhzWtNZcf/MiHP+b1+p4ta4wygaFXrlz+1H8+8fTnDRJSdX8Qgr++QCkmQhgm'
    b'JwbRVu8d/ehHPvT+UCj825LfLQMY0tl55u+/9cR3P6eElkmqqr/uJGU2IpQiNTmOsJIb/4tP'
    b'f/KBcFXkmVLeo6Uy6O/r/djjT33/c2qoRVJVz/8JUAA3SPSHqhE3PdWPP/md72Qy6TtLea8k'
    b'iZkYj77ri195+HumVKNrHn1R3DAhpPBHpyNfARQBTmZExVP3REUBois5iYkRrGj0Dn3izz9+'
    b'pywrXTd9fj4mppm/7evffOQXPVG72heoWpCkEEJAKYMQAqZpIJNJIZWeRCo9iVwujbxpwLFt'
    b'CAhQyiDLClRFg+7xwav7oet+6LoPiqKBMTfNE0KAc6c0/pQhPtqLXdtWn7v//ve+GcDEXM/O'
    b'l0RW7d+//+mugWR1uGYphChtAtfTVE6UyaQwMtqHwcEriCXGkDMycIQDQdwvSghx0wY3m3Ql'
    b'QwgIARABMCpBlVV49QDCwWpUVdUh6A8jGIyAUjbvPAR3EKpdit8dPbWmra31y294w9YH5nr2'
    b'phLT2Xnmi998/Pt/FaxrRyV5Gi0sNjYxhq7uM+gf6kYunwWRGWRZBpNkEEpmqAngSoELEgUl'
    b'tJBjuc9wh4M7NhzbgXA4CAfeeude1FQ3lig5BJZtguWG7b956NP3RCLVv5rtqTklxjBym3/0'
    b'0wMf94Sapj5gWcSYhGQyjs5zx9HTfxEOHCgeD3RPEFRyAXO4A3ABXfUi6KuCTw9CkRRwwWHk'
    b's0ilJ5HIxJG3DEiyDCYpkJRCYF1QIcvIg5clyQKKoiKR9kgHDh585IMPfHATgFSpwJDnnnv2'
    b'q6MJyxuq0cuKVaYMalfXGZw8exiGbUDz6tAUBZQxEEohBIdj24gEarF86WrUVDVAVTwgtMhJ'
    b'FhaezWUwONqDyz2dyBhpKJpWUDsKIogrQZzPWrqYExrOEQjX4sTprrbtF8//68qVqz9VEjAT'
    b'E+N7f/Pc0R3+8JKyQeGc45VXfocL3acg6xq8viCYJIEwd9HcccDAsHbFNrQuWQlJksG5Ay44'
    b'4NzIS9f9WLl8I5Y2tOHUuaPoH+2G4vGAMoYpUXYcG2UhUyDFV4MDP//lR9vbV3yeMWmg+N5s'
    b'cQw7dOi3n8vaKmVS6QU+QtwywJEXnsH57lPQAj5oPi8kRQaVGAgBHNuGJmm4feNbsaJlHSih'
    b'cBz7pu5XCA7HseHxeLF9811oa1yFfCYL4bjqIwBYtoWykRECHt2Prr6odub06b+7/vYNwCST'
    b'iXe+eOrVtb5QbcnSMpWbHDv+K/QMXYIeDED2aKCSNK0eju1AZSq2rb8LNZEGF5AyDBfnHCAE'
    b'm9fvQF24EfmcMT0/06qsyikg4AnU4rnDL7wPgLf43g3AnDhxfF/GpISx+d3f9CCE4tTpI7jS'
    b'fx56wA9ZK9iTQtVNcA5wgU2rbkdVuNYV/UoWIgQYk7Fx7ZvABIFj2YAQyJsVln+FgKb70d03'
    b'Grp6tfuDM9ZU/A/nPPjyqbN3efyRkgM5xiT09Xfh3KWXoPl9kDR1BigQApZlobVxJZrqWioG'
    b'5docHVSFa9Hc2AHTMCAgYOSzFUfjBICQvDh67PjHUaSPM4AZHOj7QP9ILKhoemmDEgLDyOCV'
    b'08+DqTIUTXONIrmm75xz6IqOFS3rwBepgCWEQGvzKlBBIByOnJGpOMsXgsPjC+Nid+9q0zTX'
    b'Tl2fAcyZs533cuop2YxRynCp6zQSmThUXS8Y2eK3BWzbQktjB7x6YNEST84dhILV8HuCyKXT'
    b'yBs516tVSLKsYDyeYd3dXe+culYMjNrV3fNGTQ+WtICpEP9S9xmougdMlmbGIQA4F1Cogqa6'
    b'1kWv2zDKsGXDTmxZuxO3bXgzKC25UDA7STouXrw0Dcy0P04mE+uHRseDim9JyRPr67+EbD4D'
    b'byh4AygAwB0bNcEm+H3BBX3RWYkADQ0taGpsm46DpuKockkIAcXjQ9/g8DoAIQCT08CMjoz8'
    b'ccZwaDBAS5IY27HR03cRkqrMcMvFxB2O2kgTKGULNrrF5Dg2ksmk+w9xk07BHXT3vIr21vUI'
    b'Bkt3Hi4JKIqGsfGoJ2/kOlTNc2IamGg0uglULmkYSikSiQlMJicg68qsYiyEACMM4bInOR9v'
    b'hlhsDM+fOAhWCAsANyaxzDxaW9aAkPI3KiiTkE5aiMfjq+obioAZGRvrIJKKUrJFQihisTHY'
    b'3IIi6QC90VwLzqFICnSPf/H3lwhAVRnV1Y3QVA8EdzNzwgGPWlkhjQCwHGB8Ynx9fUPjtI0h'
    b'qVS6kUlKybHoRGwUhFFQRkFmcWNCcGiaDkVWbsnGG6EEK5rWoK56yYxyAy8qX5Q/KENsItYM'
    b'XPNKeiqd8TAmlVRe4JwjkYoVuecbkeFcQFN0MHprGioEFy4IcKfMhVi4gScMiWSyGrgGjEoZ'
    b'k0Ao5keGwHFsGEYWjDK478w6dSiyglnFaZGIcweZTALp9CQEd0qq4s1NAoQyUEp9wDV3zQBK'
    b'S1kDIa5XsGyzUBeZg00hryG3CBjuODh7+SXYtgnbshDwhrB6+RbU1TRV5LIBNzYDgQJcA6Ys'
    b'pZyun9xs0eLWCAvnHMFAFTZ0bIOsKNBUHfFEFF2D53Dy4gvY4fkj+LyhhXhCAVwDxhGCO0KI'
    b'sgzCfAvnnN+CDX5XEttb17mFcgD11UuRtwz0RC9jZGIAHb4wnArYCsEBgTxwzcYYQnDLRXn+'
    b'z0xdXbzpmglxi863ou/B5S3gcAecOxAQCHjDAAhyZrZCnmTK7aeAa8DkggF/htullQgZZZCm'
    b'q9Jz8SHIm8ai50iEEIyNDSIaHQSZNvyuQ+DcgSKplVQ5XeI2wuFQFChKIgN+X59j5zF7R9w1'
    b'EkKAMgmaooFzPic2lBAY+Sxsp4Ky402IEILOCydw7OQh5PM5yJIC7tgYnRgEJRSRYG1ZlcEZ'
    b'Y4OjqipyFShKImuqIxe5bb6xlAEYY/D7w4gmR+eUGkIp8mYOedOAV5cX1dR4dC8mslEcPfUb'
    b'VIfrMZkYRyw9jvZla1Adqqs8kZSA6kjkJFAkMQ31DS/RMlrXIuG6gk7OPglCCUzbRDqTLBL5'
    b'hRPnApvX7cDtG3ajOlwHw8wi6K/CmzbuxprlWyAqlE7bsRH066KqqqoLKJKYuvr6X/u9quM4'
    b'DqOz5D7FJARHpKoOjEjgDgeVxCzxCoGAQDwxhoa6ZRVNdg7uUFUPljYux1LSXuBEwAUveQ/7'
    b'BiIEVj6HmsZgmknyZaBIYnTde3FJfU00b2Qwn03gnCPgDyPoD8O2TIDfqCeEEFCJYSQ6ANte'
    b'cBPlDJrySFMG16358oqDSQIC00ijZVnTCRRaYotl3FnVsfywmU2UxECSFSxrWgHbtObUacYk'
    b'xFPjmExOLDBcn50Yk9B9uRP7f/YEjrzwTOEDlA+OAEC5gdWrVv9w6toM5V+3dt1PZWqJUrJT'
    b'zjmal66ER9FhW9asbplQCgccfYNdi54aEBBYlonzl15B1s5gKNqLvGlUxMcyDTRUB6xlzc2/'
    b'mLo2A5i6+vofti2tjxq5NOZDXggOny+AFS3rYBkGuHNjlEsIgawo6BvuRjIZW3hdtogYYxgc'
    b'7EYiE4fH74cvEIIsKSi3+4AQimwqhjUr208wJvVMXb9upiS/9bbNB3Op8UKfys2Jcwcdyzcg'
    b'6A3Dyhvgs9gaShlMJ48L3aewWPEMIQSmlUfn+RfBVHcL2OPxQpbksmsxXAhIPCe2bd36pRnz'
    b'vv7BDRs2frvKJzm2ac47qBACqubBlnU7IWwOx7JumBihBLKqone4C/2Dl6c7oRZCjEm4eOkU'
    b'YqkoFI8HIAQ+PQBa5tiEEGRTcWxY3TbU2LTkYPG9G4Dx+nyH37Jj2+H05GhJ8YfjOGhoaMH6'
    b'jq0wc8as4FDGQGUJJ189gonYyILAkZiE4eFenD1/HKquY6rxIOivKtu+CBDYuRje8uY7HgMw'
    b'QxJmW7nYuXPn3wY0blnW/FIDuPWZ1R1bsLptE8xsDo41s4OBEAJJlmEKE0df/jUmYqOQKgBH'
    b'kmREx4dx5NgzEBKBrGmgzO26CvojZakRIQSZZAzrOpbF29tXfPn6+7OKhNfrO3b3XXf8JDne'
    b'P+u2yGwkILBh7e1Y3bYZVjYH2zRneCpCKRRVQ87J4fkTP0fvQFchS5/fjVNKwZiEgYFuPHt4'
    b'P/IiD83rBZPcRkdVVuH3lVeD4VxA5GPi3rfv+WdCSOL6+3P24Nm21fq1r3/jSN+EaNB9gZK+'
    b'xlSL6pWeczhz4Tgs2FBUDYTRGZ0PVj4PJ29jSV0rVrVvQjhcA0YliKITK1Njce4gkYjhwsVX'
    b'cKXvPIjCXBWSJRBCYFsWaoL12HHb20qWGEIp4mP92L19zYm9e++7A9ep0U2BAYC+vt6HvviV'
    b'R/5dr1lOSqp7FogxCZOTUXRefBFD4/0gEoUsK9NdVRACju3ANHKggqIqUIPaSCNCwWp3OwSA'
    b'mTeQSE5gLDqIaGwYFreg6h5IigIquY0DgnOYhoHb1tyB5c1rStrUI4TAyGUQVjLpv/zMp7fr'
    b'Xu+rsz43D8rqoUO/PvjfB57bXVXfVpaoUkohuMDIWD+6ejsxHh+BAwdMktzWM0IguNsmZpum'
    b'2+vCC3XXQsVfCAEqMciKAibL02rNhQPBBSQqIeyrxtZNu6AqWkkSI4RAauyyeOgTH/2X5e0r'
    b'PjvXc/M2QAvOWx574vFfnLo0ujJY3QRRZqLGKIPDOSYT4xge68XI+ABS2YRbpyG41tcrgBmH'
    b'vwSmwx4Bt4wqUQmaoiMcrEFtVSMioVr49ECh4bEENSIU8eHLeO87dx/atWv3n+AmB05Lapk3'
    b'jNwbv/bwN348MCmW+AKVbbnSQqelbVvIZJNIpuJIpONIZxLI5bOw7DzsQlIIuM3OsuwWu316'
    b'EAFfCEFfGF5vAKqiuSfbOC95L4kQithYL3Zsbn/lA/v23Q2QObvCgTJOn8RjE3u+9NWHf5Di'
    b'AZ+3TA8w2yRpQVKmWt4d51r9FnDb1xhlcLe7XBWq9CwBIQzxaB+2rW/u+sC+fe9gTLow7zvl'
    b'MBkaGrzvm9967NGU4w16A5Gy1Wqeqdyw67A4hzkoJscHsG55zbkHP/zhP1VV7WxJ75XLfDIe'
    b'u/eRRx97YmDCrg5W1b+Oj+e4rfjx0at406b2c/v27dvLmHS+5Lcr+SrpdGrrU995+kdnL48s'
    b'CdUuAy20s75eiBAKyzKRmejF23Zt+/2999z7IcrY1bLGqHRBjmO3Hzhw4Ae/evbYZjXYBE33'
    b'LbJqVUJuUJhKjENDmu99x54fbNt++4MAsmWPtMAvrb/aefazP9p/4FPDcdMbiDSCUfaaqBeh'
    b'FGY+j3RsAOs7mgbuf897/qGmtu4JABVNZlEOpBu53PoDB//n0eePndzK5SDxBqoLu4W3GiD3'
    b'fJNtWUjFRxDxEnvP3bv+a8eOOz4DILagkRfRNtCR4aH7fnPot//28tkLLXnhgTcQgSy7VbXF'
    b'tEGEUDdtMLLIpsYR0infsXXz8V137vprr893ZFF43AKjqY2MDL/v2PHjD758qnPreMKQZS0I'
    b'1RuAJMmFYFYUqqCl8J5y466Bt8w8jGwCwkpjaX0484bNGw9t3779Kz6f/9kSByyJbuXPpMDI'
    b'5drOnz/3yTOdne+60ju0dCKRkThRICk6JFkFk2S3vR6kEP5f6yoUws2jHNuCbebg2DmoVKAm'
    b'4jfbW5ed27Rxw5MdK1Y+BUIq+omC+eiWAlPMxzTzywcG+t/S09N77/DI6OaJ2GRtMp1VMlmD'
    b'cpBCXcb95RDOHciMQvcoTsCn52trIoOtzc2Hm5ubf1pbV/ciIXT4lk/4NYw/goI7tdlcLsI5'
    b'DwJQ4RbOHAhhyLIcVzVtnBAaxR/4Z5iA1xaY1zX9L1J0cGN8ZkP0AAAAAElFTkSuQmCC')
index.append('Cecilia_about_small')
catalog['Cecilia_about_small'] = Cecilia_about_small

#----------------------------------------------------------------------
cecilia_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAdCAYAAAC9pNwMAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABUtJREFUSInll0tsXFcZx3/fuY+545nJZDw2fsR1sEdpE1Oi'
    b'gEIRIaqC0gpoQAqO1EVVVY1UFqVNVcmoimARsoFIrRoEC7LiobJAIaqSSk0FERJGkUXs1AoN'
    b'hBCl7dhuYwc/JuPM3PHcxzksPLacNjgOBWXBt7znnv/vfN/9HueKMYZ7YeqeUO8l2P4vaKQi'
    b'aK/VaslUMukrmAL8/xXY/evly0+ePXNmf3F0dLsulRI3ZmaktbPT2LncQueDD458affuX27t'
    b'6/s1EN5OQO4yueTdYnHvTw4d+mHl3LnNG6KIlkQC17axlSKKY+pRxGwQMC5Cx6OP/n3/wMD3'
    b'7i8UTgG3gO4KfPKNN15+/dChgS3VqrSvW4cWIf7IfgGUCMoYJstlLnqeeeLIkZe/uWfPwZXw'
    b'tYLVb0+cOPr6wMCBr+RyohwHbQxiDBiDAbTIkiDKGBBBLAsdhgzOz5v+V1758b7+/oEl+JrA'
    b'Fy9d2n9k376f7/I8sCwMIFqz4DhUcs0EzXki10VEcLTGrlZwZ2fJzJcREUwc88d6nYMnTjy9'
    b'ta/vV2sCR1qvf+mppy51nj/fsT6TQRsDWjPXnGfhgc14+Tzq+hT25DVAiDo3wIYu9MQYubfP'
    b'IyIoEcqVCle2bLn20+PH+1zbLt+xjoeGhl7yh4Y68g2oaM1cvoV4+xfo6C2QHR8nOzJMZmKC'
    b'zMQ42ZFz2ONFnKYUNMKvjaE5nYYLFzpHRka+C3duINbQ6dNP9zgOUeOb1hIJos98lq6uLlLV'
    b'KupvFxfDaVkYy0IZg33lCtXS3K2RM4Ye22bw1KlnAGtVcBBFfZOjo+3rPW8xI4ym+qk28hs6'
    b'yWay6LEiBMGyZwBGKRLVCsnxccrZLHFjzQC5pibGhofbFoJgy6rgmbm5QjQ9LY692Gc0Ai2t'
    b'ZNPrcCxFNDONqI9LaBGm29qoeR6y4rljWVjlsszduNG7Krhy82ZzXKste2SUwkml8FwXSwSJ'
    b'Im6XmmIM6TjCS6WRFdFAhNj3qdy8mVsV7LhuIPaKrmoMSkApBQha5BaPAASDsSySpRJhJkOY'
    b'SCzW+9K6beO4bn1VcGtr6wduczNxHDc80eD7RFojloWVzfLRcjQIGMNCMok7OYlTq2EaXsdx'
    b'jJvP09ra+uGq4LTn/SVTKIR+EACgDKipKfyajzEGt3sjH3MZsOKYykIdqzSHteJgfhCQKRSC'
    b'tOe9c6dyKvXt2nXmWq2G3SiZxNQk88X38esLJHp6obMLwpClNqzimPlMBl3YhOW6yzlgi/BB'
    b'tcqmHTt+B9y5gex+7LHD13K5OI6iRYE4Rob/zPS7VwmVwtn5MPX7uomVTSyKcr6F2rbPk0+n'
    b'SNTry+AoDPlnW1v0jf7+w7CGG0hbPj+8+/nnj4/OzOCKLGZ2pYL+w++ZPfsnglqNePtD3Nix'
    b'k+mHvoi/7XMkLQuv+D5WGIIIrggXSiW++sILv2nJ5d6GNQ6JMI47vn/gwFnrrbd6729pIWxM'
    b'JbQmdl1MKkXkuBhjsIM6lu+jogiUwhHh8vQ0zt69Vw+/+upOS6nrawYD1IJg4+EXXxysvfnm'
    b'xq35PFjW4ixeGo9LJoIRwRKBOOad2Vm8PXuKPzh69OFkIjGx/NrdXAQirTf+4tixnw0dO/a1'
    b'T/u+tKfTOLZ9S8vEGMIoYrJS4arrmi8/++zpbz/33HdspcZXat3t1QeAq8Xit06+9tqP3hsc'
    b'fEBdv47TyPpQa8KmJkx7O5sfeeQfX3/88YObenpO3k7jPwI3zFqIom0TExPbPxwb6wWSBqpd'
    b'3d3F+7q7RzzbvgDof7f5k4A/kf3//Un8C1j2Wltb4vwkAAAAAElFTkSuQmCC')
index.append('cecilia-click-trans')
catalog['cecilia-click-trans'] = cecilia_click_trans

#----------------------------------------------------------------------
cecilia_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAdCAYAAAC9pNwMAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABNxJREFUSInllltsVFUUhr+99zlzzvRehlJotGVaKwgRBGtC'
    b'BPESY+KFRB+IhIiGGJQY3zThAd8MD4g+EQ3RGIkkXp40RCEBo2AAAYlcZNQWKPfSMr1Mp7eZ'
    b's8/Z24eZDI1ibfHBB9Z5O9lrfftfWWvtJay1/B8m/xfqbQl2btVR66CtvePc2jOdFx/LDA63'
    b'SiWViUxUU11xprW56fs5d7d84rqxY//kL6ZaXFEUzd9/4KfNu787+PSlrl4iKxBCIgALWGtQ'
    b'wnJnQ4KnHl/27cPLlmxQykn9J3A63bvqw+1ffHo8dd51vTiOUkXc38ISRhE6P8Z985P61bWr'
    b'XqybPv2LWwL39Fxfs+m9bR9f6xtxfc8HLEIU1FprMMYU/ymklGAtxlpy+RyzEuV64xvrX66v'
    b'n7FjSuAgCJZseveDg7+d65a+5wEWKRVjuWH6M90MjvQR6BwAjuNR5ldQXZ6gtnoGIMjlc8xr'
    b'mWU2vvna0lgsdhgmV9Vi5669W1MdV0pQISTX0hdIdR7hcv9ZUJL6RCMzEo0IR9CTvUx35lLR'
    b'3eJ7PqmOK3Lnrj1bATEp8NDQ8Kq9+4+2eX68oFRIutMXuJRuR8QVd9TfxdzGxcyqS9JQl2Tu'
    b'nfeTqJyJwXAjmxbPj7Nn39G2oaGhVZMCn/g1ta4/M4qUAiEEI2NZrvafx6ssp6oiwayaJgQC'
    b'YyKMiVBSMbO2EUJbBAsApJQMDI5y4lRq3WTA5SdPty8XUhVyLiS9mWuImMD1PGri01DSwY6r'
    b'bGMN5fFqZjfcQy4YxdiopFpIh5OnO5YD5ROCrTXJdG9GKVUAGxMxks/i+j7SUXhO2U2byVjD'
    b'tf4L9A52YY1BFFUrpbjeN6CstckJwVrrmr6BTKE9AGMMhgipFEJIlFRwk64QgOO4lJVVIqUq'
    b'ZURKSf/AIFoHNROCpZSB78UY33JCSIQQpYsUxfzNEpUzGQmyBGGudN5ai+/FkFIGE4Idx+1K'
    b'1FYXhwMoqXBVDGMNFksQ5UtpvKFWYLFkhnvxZJyY45UubowhUVuN47hX/624riSbGq6GkS6p'
    b'rSpLEAUhWMuIHuSvA8hiUdJhNJslrspR6sY7FIaaZFPDVeBfwbQtWvC5KwtarDUkqurxhEeo'
    b'NcPBENmxfpRUiOKnlEN/poe+4R6EFONGucBV0Lbo3s9gEn3c0jz7nYXzmrP5fB6LxXFiNCZa'
    b'UVqidZ7LA+e4nulCRwFhpLned4ULPb8Tr6gg7leUMpIP8iycl8y2NCe3TAoshEivXrlii++C'
    b'MRZrDWV+FS1185kWqwMLF9PtpM4f4dS5Q5zvTuHGPGbWNuE6HhaLMRZfWVavXLFFCJGGyb9O'
    b'3v4Dh3Zv2/7Vo9L1kUIUK1Wgwzx5PYbWeSzguT5+rAylHGzxhTI6x/qXnvvh4YcefBLITwUM'
    b'4O/78dDej3Z8vSzEIea6gC1UtbhR24VloBAz0BqF5pU1zx54ZPnSJ4CxUianuIGUdZw5+/aO'
    b'L3e+3t7ZFUM4OI6DlBIhCrPEGEMYhmBD5jQ3BC88v+L9Oa2tbwGj4wNNefUBMCaa+8vxU5sP'
    b'Hzv1TOelLpnJjqB1iOs61FSV09zYYJa0Lfhm8aIFG6RUf9wsxi2Bx1lNGOoHBrNDzTrQFW7M'
    b'Ha6uqux0HPdnIDOR438F37Ldfgv9n0R6M7hH0MziAAAAAElFTkSuQmCC')
index.append('cecilia-hover-trans')
catalog['cecilia-hover-trans'] = cecilia_hover_trans

#----------------------------------------------------------------------
cecilia_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAdCAYAAAC9pNwMAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABIJJREFUSInlVk9sFFUc/mZmd2Z3u2wX625pUiK029L634QW'
    b'pJRUm4AIaMJFICkJMdWYePGgXDAe9MKhmhgTMYEYDmpEo6JVREnFtFXSVozdJRaYLSnt9M/u'
    b'zi7bXdudmTfz89A43bZLu9QDB37JO7zvve/75v3evN97HBHhbgR/V1zvSWPHaom5XG6zqqpH'
    b'crnZp3leqHE4HAJjhmlZ1nWXy91VVlb2scvlGrgdn7vTn0vX9YcUZey4YRh7/P618Pl8EEUR'
    b'HMeBiKDrOqan00gmUxBF5/eVleuPiqJ4ZYkQERXdUqnUgUgkrCeTSSomVFWlcDisp1LJA4u1'
    b'ijZNJtW2SCSsG4ZR0MRkJjHGluCGYdDg4KCuqmpbvl5RqdY0bWs0Kvdu2lTHC4Jg4xNTUzj/'
    b'axd6+/swFY/BAmGtrxS1VSE0N25By7btAADGGIaG/rZqamqbJEm6VOwec1evDvVVVq7fXFJS'
    b'YoNffHcW7536CGOxSbRs2YbWpmaACOe7L6LrUi9at27HJ+9/aM/PZrMYHR0dqK+vbwSwcooz'
    b'mcxBWZYXpO/zs19TbctWCrU2UcfJE2Sapj2m6Tq9cuwN2vdi2wKciOjatWuUyWQOEtHK51hV'
    b'1fZgMGj3R0ZvouPkCXCSiIbHn8CrbUfA8/MyotOJlw8ehkeUYJrmAq3y8nIkEvF2YOUCUqJp'
    b'uR35Kf7mpx+h/pOB0+3CzqYdEEVxCemRunq89drrGL45At0wbNzr9SKXy+0AULKsMWNsoyA4'
    b'hP9WRES4fCUMye2CJEmoqwoV5Gm6jg9On8KXP3TCMHQb53keguAQGGMbVzA2/Iyx/A9BOpuB'
    b'Q3SC53l4PZ7bcku8Xmzc8AAkUVqAW5YJxgz/ssYcx+s8z+X1OQiCAI7j7JUV5gH7dz2L3//8'
    b'A2OTE4s153SXM3Y6neP5x83hcKD8/gBMZsJgDKOT4wV5umGgq7cHD1bXYF0guGDMsiyIoqgs'
    b'a8zz/BgRFE3TbKxly5NghgEQoedyf0Gez7sGmVQKjQ8/Bpc0n2pNywEgheO45Y0BoLS09LNE'
    b'ImH3d7e04tHqWui6ju7L/egZ6FvCudjbgzPnOrG4NMXjCfj9/k8BrFyrGWOBcDiczi8GV6My'
    b'7W0/TKFdzdR8aD99e+E83UqnKT09Tee6LlDDvp3U+NwzpKZS87XcNGlw8K80YyxQdK2Ox+PH'
    b'Mpnpt6uqqm1sKhHH6a/O4OffujExOYX71qyZu8HSaZQHg3hhz/N46VCbPV+WZZSW+t4MBILv'
    b'AMXfx1I0Gj3n8XieqqioWDCQyWYxoowhps5tx7pAEBsq18PjdttzxscVzMzM/hIKhXYD0IpK'
    b'dV5zybLcfePGMFmWVfBqXByWZdHwcJRk+Xo3Ebnz9e7oIUBEHkVROiKRiBaLxQrev0REjDGK'
    b'xaYoEglriqK8S0SexVp3/PQBAF3X6yYnJ47PzMzsdTic/Hy9nnv6GAazPB5PZ0VFxVFRFIcK'
    b'aazKOC/8mqY15HKzVaZpeXmez7rdrmFJcvUDuLUc8f8arzruvQf9v42ByFQYvgT4AAAAAElF'
    b'TkSuQmCC')
index.append('cecilia-normal-trans')
catalog['cecilia-normal-trans'] = cecilia_normal_trans

#----------------------------------------------------------------------
close_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAKtJREFUOI3tk70NwyAQRp+jDJAN7DT2GGkpM4I3gBE8Apsk'
    b'nb1Faqp4BDIBKUyFzpBIFCnySRR3fDzu+GlCCNTQoQrlD/pIxzQxmOUE3GPYAl1i8UDnrHpl'
    b'K3JWeeABXAQIgE0hIihqAlYh7wErLRBBccdRmDJSNQBN7mUPZrkB1xiuzqrznrd0ayNbO7C1'
    b'u68QQnb0eta9np8lXxEUYW3Jkz2jb/R7X6Qa6A02643KV+L/pwAAAABJRU5ErkJggg==')
index.append('close-hover-trans')
catalog['close-hover-trans'] = close_hover_trans

#----------------------------------------------------------------------
close_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAIxJREFUOI3tk8ENwjAQBCc0YDqATlJKSqAVOqEFOqAEiwoC'
    b'FUw+fiDs2FaUDxIr7edub3T3uEFlDx12ofxBm0FH4J4cAb88A6EH9AIewAicC/0r8M6qaslB'
    b'jeaaUy+bWQOhjgXQtJavgVBvH5BYy7ZAIZ1T3aYHhHppbaMy2Pe0J+BZC/SCmvqNF9mkBXQJ'
    b'M9Cu1Q41AAAAAElFTkSuQmCC')
index.append('close-normal-trans')
catalog['close-normal-trans'] = close_normal_trans

#----------------------------------------------------------------------
delete_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAANdJREFUOI3dk70NwjAUhD8QfbIBdC7JCNC5S9ggG+ARMoJH'
    b'YISkc0k2SOsuI8AEoeBZSJAfQCkQr7Gei+9Od/ai6zrmmOUslP8GrZ4vlHEboAEiYO+tPivj'
    b'YqCVu4O3upx05K1ugUJWK2chkKoPArAYql8Z1wBboAJS4AokIvQyYxnlcqbB1RBk1JG4KoMb'
    b'b3U8IjrsSELfyRop47KvQNyDjoA67NLe+yBRDwFnAlvzaHMaJKqh9txbfeEe/BU4KuOSdx0V'
    b'ol6HNyNtBfipDzTa2ifze5/2BlE8SAXEJVqGAAAAAElFTkSuQmCC')
index.append('delete-hover-trans')
catalog['delete-hover-trans'] = delete_hover_trans

#----------------------------------------------------------------------
delete_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAJpJREFUOI3llFENhDAQRAcUVEIlIAEJlYIEJCDlJCABCScB'
    b'B+8+2CZ7pDQH4YubpGl2uvu6mzRtAN2h9hbK/4GipFUSknrzgvNSkQSU1sCmxeLJ4tdB/iFI'
    b'BsnFACsQr4A6vjVUcqsg7bqp5tYOowGy0lVQ7ma2/Q2Es6DkRgoONp0BBbvdj+PH7H4F5Tcz'
    b'7/zR/KUEanjsN/IBfIUTn7eS1Y8AAAAASUVORK5CYII=')
index.append('delete-normal-trans')
catalog['delete-normal-trans'] = delete_normal_trans

#----------------------------------------------------------------------
edit_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABMAAAAUCAYAAABvVQZ0AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAUpJREFUOI3l079L1WEUx/GXWWAIbhpCCg3yxUGQSII2DeQB'
    b'N4cGISVEITT44tQk2RRU9KyRoz/+AKm+SzjUoIOCJMkzqEN/QS2Cy2243wtx+d4WHYTOcnjO'
    b'4fPm/HraarWay7Jrl0b6f2DXmwNZXnRgFY8wk2LYrBJmeXED/ehOMey0qmwDR3iK+1leDFeA'
    b'OvEK+9hqxKtg99CHj7iJjibQNL5jCV8x37JNPMZo6cdxjJ0sL27hdRn/iUV8SjGcNoRtVUeb'
    b'5cWdsroejKELveozWsfnFMNus64S1gRexWz53MNIiqFS1KqyuxjAEG7jBIN4gG/YxJcUw9k/'
    b'YVleTOIhztXn8jzF8LbMLeMZOvEea/jRgFZt8w1+4QXeqW8MpBheqi9nGwv4gKlGvgp2UPon'
    b'pf/9dzLFcJhimMAc2rHSss2L2NX96FcX9gdUL2F//BM8JAAAAABJRU5ErkJggg==')
index.append('edit-hover-trans')
catalog['edit-hover-trans'] = edit_hover_trans

#----------------------------------------------------------------------
edit_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABEAAAAUCAYAAABroNZJAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAASFJREFUOI3dk70rhWEchq+XlJNiI4U6yaAoIWRRVpvNoiRK'
    b'NmIUi2Qx2Uzy8QfoZDKxKJ0SZTvKajNQx3AZPC9vr/cYnIHc9fSr535+V/fzFalUq5qqCf8b'
    b'Ug8cAGVg6pueOqATGMmCHAF3wAIwDPRlABqALaAInGRBBoF2oADkQrKkpoEbYAk4B+Y/HDUe'
    b'Y+q6uqLeq6thvkXd910P6qKaT/QRpR5bPqRpBsaBRqAV6AAOgVPg8ssmk8TU2PNTV2pUaW06'
    b'ST/QBfQCbUAJ6AZGgQvgGDgDXiolmVR31R31VV1OeGvqo/oc/AE1F/tJSEndVJvUbXUoFbtH'
    b'LahltajOxl7yiq9DnQn1KXV8t8AEMAfUAhuxkT6TH+lvfsDfhbwBDZwChidQy5sAAAAASUVO'
    b'RK5CYII=')
index.append('edit-normal-trans')
catalog['edit-normal-trans'] = edit_normal_trans

#----------------------------------------------------------------------
filer_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABPBJREFUWIXNmGtoFFcYht8zOzuT3Un2kmw22WRjyCqpIdZL'
    b'sVkrtbRC441Sf6QttjT9YYMlARVTDJYWRERrwdpgS0MQQQTbHyoIXqLWatUmUlNtkxaTmk3N'
    b'msvGzd6zs5vZnTn9odVUJdnJmuoLA8Nw5puH75zvPd8ZQinFsyzmaQNMJlbtC2I8Dr/fD0yQ'
    b'eVlRYDKZYMzKSgsOUAnY3d2ddebQoTeCN29WaijNfuwgQjAiioGo2Xx03YYNp1+YPz+eDiBJ'
    b'dQ3e8fuf+7qh4aexq1cZTzR6JCCKNxiGoePflynFrJycV57Py1t9sa9v9JbZfGJnY2Pt4kWL'
    b'wlMFTDmDv7a1rWZ7evjLXu92t17/7fKqKlGv00FRlLsDCIFCKSxuN+UikZULios/N3u9zg1r'
    b'1x7ctmfPBysqK4PTCpiMxfSEUrFXFP9ev3lzfF1NDTQMg4fz37lvn3Lz+HHiDoVCvmRyUwXD'
    b'XNje0FBHKf1i5bJlCbWAKVfxvzCcVkuL7HYIej0yMjKge+iiihIAIfys3FxbrySNSCzbNE+W'
    b'126try89d+ECq9bWpmQzsiz/5/7OwAAJBwIAAM5ovJhUlD8sHFf77uzZH0UTCVep1Rp/UaM5'
    b'9s2OHXUjPp8w7YDj1XXtmnFXXV3FsQMHdABQvGTJgKW0dGlsdHS9WZKcK4uKNuXwfGxhQcHM'
    b'XEn6OOT3F6uJr9oHH9Zvra22P1tbZ8oMM1xVU3Mr2+HAyw0NPldLy3eRoaHDjEbDd3R05IZv'
    b'33YNJZMhGRD/V0BFkiw5BkN5wOvtDQeDt3SCAKPdjnnV1ZAlKQEgcWXXLr2vqws+WaZJRVG1'
    b'CKc0xYSQBwEUJWuG0fh6UhQLhwcH7z/XcBy4zExwmZkgLAsCgDwm1mRSnUFCCCilGO7vh9vl'
    b'gtfj4Ry5uWU0FHr7SFPTD6FAIFRSWgqdIECr1ULL8w+8croBCQANy6KrvV2ItLR85uvtFeOE'
    b'2AtNpkynIFQN9vXN/XHnzoM6i8XD6vUhlueTMseFOzs7B+1aLTAFUNUZZBgGnv5+OeJysVpZ'
    b'LpEI0cNkAgghGp43Bjyekr/6+phYMqkjhEQlQI4DGcU2m2o41YAUgJxMYu7ixXGuvPzTS2fP'
    b'sjylK+Ky/KbL7x+62t9fn+9wnHGuWhW12mw002CgepOJnjx82Jro6JiwA3oigMBdY87Jy8Nb'
    b'tbXiexs34vvdu6M9p06FOgOBc8urq8++U1MTtuTngxByv5iut7fDc/26argpAQIApRQMw0An'
    b'CADLxnpHRs7zZvPJ1dXVYWtBwSPj0ymStHcSotUORiSpRTAYfhcE4YmfH9IGNJjNg6FotMda'
    b'VDRszH58D5uOpjTF4426YunScOWaNb+UO52yhk17Y3pEKUeklIK515SOB7Q7HHTL3r0Tt/WE'
    b'gNyLMW2A0UQikZBlrjAjQ/tzWxuZt2ABOK12wo8SQjASDEJ0u3kAiCQSEgFUVUzKgLYZM87v'
    b'DwS2vFpYuNl/6VJw/40b3TzPT+ptZGyMF8bGPjk5MOA3lpWdyLdaVbX+KQNWLFx45aWqqteO'
    b'Nje/X6LTfcn6fCaF0gn3f0IIZEBxhUKdo4Lw4Vf19Zezs7MjagBTPtUBgBiLoam5mdu2dWtB'
    b'LBKx0EkaFAJAoVQumzNnoLGx0eusqFAopRCE1JtqVYBPQ8/8r49nHvAfh6kkrQ1tQ5YAAAAA'
    b'SUVORK5CYII=')
index.append('filer-click-trans')
catalog['filer-click-trans'] = filer_click_trans

#----------------------------------------------------------------------
filer_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABL5JREFUWIXNmGtsFFUUx//3zmNnt93OLm2hpYU+kJeFgkpK'
    b'VEJArcGWgEZFQgRFISamRhMlPhGNhhgaozEhwUTE2g8SNVZAHqEYrJaHEltoKba0YFvaLXTb'
    b'fXWnuzududcPqJTQpDvbovyT+TC5j/Obc+8959whnHPcyqL/N8BoEhMZxBgD4wAZoY0DECgB'
    b'ISO1WpclQMMwlV+b/iyta+54MBqNuUaCYIwj1ZXsXVg47fM5+Vl1YwUkFvZg/p6f6mu3fFrF'
    b'Ojz9JwzGmulVh10ngZL5oiQumZGT0fv6+tI9xQsLNnEOJktCQl6NG9Af1F58+p2dm4+dOV85'
    b'b/rU94vvLuhPUmSwYeNlUUBDa9czv5xufWMgEp1HQba/9lSJ8Xhx0XPuFIeZCGDcSxyOxOyh'
    b'cER3O5OaylY/4CtdVAiB0utcSAnBt0dOsa7egPjo/Qu0rTv3lZVXHDotS+KatcvvrRQF64Dx'
    b'n2ICEAI47DaWl5UOWRIhCBTisIdSgmSH0u8LhicXFeRml7/0RFiyieVbd+3ftGtvrWKa7CYC'
    b'/iPOYZrmv6+mydDtDRB/SAMA3DkrpyZ3cmrtlh1V1frQ0JrC27JaAwOa/mHlwZPfVJ8qMUzT'
    b'ks0xx8H6lk71hW27i77cf9wOABlpamjzxpX3pbmdqyp+ODaVMV4yf+bU41pEL/xiX215IKTl'
    b'WJk/oTg4XMcaL2YeP9cxjRLzyoaHF7cn2W2YlZuJ7a+ua+wLhhsJgIvd3uTnt1aUmYzTIYNZ'
    b'sjlmDw4ZLC0lRS3wBrSMwMDgtYkpwUS3E+luJ9xOBwglIBSWQ01CgMONMBCnmp5ZrOksy+P1'
    b'jdjfZByJpnzLS0wIAM7R7unDpZ4+XO4LymmTpswOgq/a8V3tEX9oMDgzJwMORYYkClBsMhhj'
    b'SDTzWQMkgCQKqGvpdPzcOrClyxcbJGY025XtTE5KmftYp7+v8IPvz1amOc9ftoskqEjUUESE'
    b'An5fWzAcQbrLeWPqGVdAAJRQdPf6zXNtHpHIjjzCdIeLA4SCKCJVe4KhvM6OADX0mJ0SaGCG'
    b'CRZTDH0IhJARC4zxA+SAYTIsnJMfA/hbNb83i1ywPWTo0ZUB76UeT1vTy/mZrsPLl07XMlJV'
    b'nuJwcLeaxH0hLXlbxUGYzHqgtuxBwzQxaUIK3nx2xeAr65bho9012oGGzqC/u+3HtcsWVG94'
    b'ZGkoI00FwbXD1NLeA1Gglpc3IUAAYJz/nd4UCASR/svdR1126cCTJYtCk9NdN/Q3WeJV+5jj'
    b'oCwQjx4NH1Id8hmnwzbu94cxA7qddo8W1tqyJ7mvuNXk8WC6TmNOdUsWzAqtLr7rt6Lb80xR'
    b'GP8rTtyABFfLZ0IIBHoNJD8rnX+yaU10tMGc8xHq79EV9ycrNjlmt0mSbpiIRHVLRhrPX1IC'
    b'A4Pg4IZVzLg9OEFNOnzH7Nx365rbN3z8VXX9ybMXukZzCiUEV3xB29FTf2weGIz2ZqaqDS6n'
    b'PXhTACkhTWtL75lX39xeVlPX8vXJxjY1nrxgMsZMxtqnTZm4ff3KxVV2m9xnBdDKrQ4AcLHL'
    b'S977bO+Mwyca58qSNOoW0Q2Dz5+Zc+HtjSsaigryDKvllmXA/1q3/K+PWx7wLy0N8w8GixGz'
    b'AAAAAElFTkSuQmCC')
index.append('filer-hover-trans')
catalog['filer-hover-trans'] = filer_hover_trans

#----------------------------------------------------------------------
filer_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABORJREFUWIXNmF9IW1ccx3/n3Jvce3OtpiP4Z5nVVlkQqQXF'
    b'KaVVNuiqo6IPsoeVISXQTktH6XSyEemLUGvpk223SqGUgD4prtDh1NFNhaClhXSry4LR2LRG'
    b'm94Yo8Y095579tCZNdtsE6u2X7hw7uEc+HB+53x/v3MQpRTeZuE3DfAqsYlOWF5eBr/fDxhj'
    b'WG/1FUUBvV4PO3fu3F5Ah8Ox4969e1Ucx33Mcdw76wHOzMwsOByO3rq6up+Ki4vDrwOI4t2D'
    b'c3Nzpr6+vl9NJhN2uVw9s7OzfzAMEzNZlmUoLi4u279/f01XV9fyzZs3b1ksloaDBw8GNwoY'
    b'9wrev3+/Ji8vj+vu7m4dGBj47vDhwyGdThcNM6UUFEUBSikVRfGTioqKNqPRWNLS0mJtbGys'
    b'O3LkSGBLATHGOp7nQ2NjY9MNDQ3h+vp6wPifM0YpBYQQaLVaFSGE7Hb7otvtPnPixIlfOjo6'
    b'TlJK26uqquREAeM+xRhjIISARqOhmZmZIIoiCIIQ/XQ6HQiCAAzDLGCMucLCwoyRkZGnwWDw'
    b'+6NHj5ovXLjw/tDQEJuorSVsMwghIIRE/xVFAY/HgyRJWusaBoDfs7OzG9ra2r4IBAKu0tLS'
    b'cH19/Q83btw4KUmSuKWA/9bY2FjK8ePHP7hy5Yrwd9djAPgIAL40mUwlTU1NZ/bs2bNaXV2d'
    b'U1RU1BgMBrO2FXBkZCTDbrfnDA4Opi0tLa11SwDQDQCfYYwPTUxM1DqdTjoxMbEYiURC2wqI'
    b'EDLk5ubmS5KU/kKY1yQTQpZtNtuKx+MBt9tNZVlOaBNuCBAhFG1zHLejoqLiEMbYODk5+Z+x'
    b'DMNE56y1E1HCqQ4hBJRScLlc4HA44NGjR9pjx47lra6ufnr16tWhhYWFxfz8fEhKSgKO44Dn'
    b'eVBVNWGwDQEihIBlWbhz545ICGnBGIcMBsN7OTk5SWfPnq0dHx8vsNls1unp6TlZlhdZllUk'
    b'SQpOTU3Nms3mmJXfEkCA5344NTVFQqEQm5WVtdvn8+kIIcCyLFJVNeXhw4e7nU4n9vl8wrNn'
    b'z1bm5+dJWloav5HwJgxIKQVVVaGsrCzs9Xot169fZzMyMir9fn91T0+P99y5c1+lpqYOlJeX'
    b'r5SXl9Pk5GQqiiJ98OBBKiFk3epn0wABnhcERqMRTp8+HbJYLNDZ2bnS29u7eOnSpZ9ra2sH'
    b'm5ubg0ajETDG0ZBeu3Ytxty3FBAAQFVVYBgG9Ho9KIqy2t/ffxsAfjx16lRw165dMWMJIRuG'
    b'A9gEH1QUZdbtdvcLgmBPSUnZ9PvDawMmJyfPer3eyezs7HmDwbAZTDHaUIhftIvKysrg3bt3'
    b'xw8cOEA0Gs2mga0pbkBKKTAMA4qixACaTCZqtVrXLesZhgFKaUztuCWAgUBARghpCwoKNMPD'
    b'w2jv3r2g1Wqjher/WQhCCJ48eQI8z3MajQZ8Pl+EYZiE0krcgAaD4bbVav3GbDZ/PTMzE7Db'
    b'7X/yPP9Sb6OUAsdx3L59+75tb2/38zx/Kz09PaHSP+5LUzgcZs6fP180Ojr6eUlJyYeCIOhV'
    b'VX1p7kIIgSzLqs1m+83lcnVevHhxtKam5umWAAIAhEIhuHz5sra1tfXdSCRiAIBXJldVVUlu'
    b'bu7jjo4OX2lpqUopBVGMv6hOCPBN6K1/+njrAf8CvsEoAJzTrm8AAAAASUVORK5CYII=')
index.append('filer-normal-trans')
catalog['filer-normal-trans'] = filer_normal_trans

#----------------------------------------------------------------------
Grapher_background = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAACcQAAAV4CAIAAAALudsQAAAAA3NCSVQICAjb4U/gAAAACXBI'
    b'WXMAAArwAAAK8AFCrDSYAAAgAElEQVR4nOzdoRHDMBBFwbNrUP8VqQgV4CICDPN4AnbRg+Ka'
    b'uX+dc2bmeZ6ZWWtprbXWWmuttdZaa6211lprrbWemXsAAAAAAAAA+OIzFQAAAAAAACBce+9f'
    b'vwEAAAAAAADg79xrrffs78xorbXWWmuttdZaa6211lprrbV+25lfAAAAAAAAgOAzFQAAAAAA'
    b'ACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhM'
    b'BQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAA'
    b'AAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAI'
    b'NlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XW'
    b'WmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa621'
    b'1lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmut'
    b'tdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lpr'
    b'rbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY6'
    b'2plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8A'
    b'AAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAA'
    b'AIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAz'
    b'FQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAA'
    b'AAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg'
    b'2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUA'
    b'AAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAA'
    b'AAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZT'
    b'tdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lpr'
    b'rbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZa'
    b'a6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXW'
    b'WmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa621'
    b'1jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZ'
    b'XwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAA'
    b'AAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA'
    b'4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUA'
    b'AAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAA'
    b'ACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhM'
    b'BQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAA'
    b'AAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAI'
    b'NlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XW'
    b'WmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa621'
    b'1lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmut'
    b'tdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lpr'
    b'rbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY6'
    b'2plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8A'
    b'AAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAA'
    b'AIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAz'
    b'FQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAA'
    b'AAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg'
    b'2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUA'
    b'AAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAA'
    b'AAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZT'
    b'tdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lpr'
    b'rbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZa'
    b'a6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXW'
    b'WmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa621'
    b'1jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZ'
    b'XwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAA'
    b'AAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA'
    b'4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUA'
    b'AAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAA'
    b'ACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhM'
    b'BQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAA'
    b'AAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAI'
    b'NlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XW'
    b'WmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa621'
    b'1lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmut'
    b'tdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lpr'
    b'rbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY6'
    b'2plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8A'
    b'AAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAA'
    b'AIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAz'
    b'FQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAA'
    b'AAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg'
    b'2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUA'
    b'AAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAA'
    b'AAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZT'
    b'tdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lpr'
    b'rbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZa'
    b'a6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXW'
    b'WmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa621'
    b'1jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZ'
    b'XwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAA'
    b'AAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA'
    b'4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUA'
    b'AAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAA'
    b'ACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhM'
    b'BQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAA'
    b'AAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAI'
    b'NlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XW'
    b'WmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa621'
    b'1lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmut'
    b'tdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lpr'
    b'rbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY6'
    b'2plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8A'
    b'AAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAA'
    b'AIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAz'
    b'FQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAA'
    b'AAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg'
    b'2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUA'
    b'AAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAA'
    b'AAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZT'
    b'tdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lpr'
    b'rbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZa'
    b'a6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXW'
    b'WmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa621'
    b'1jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZ'
    b'XwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAA'
    b'AAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA'
    b'4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUA'
    b'AAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAA'
    b'ACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhM'
    b'BQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAA'
    b'AAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAI'
    b'NlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XW'
    b'WmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa621'
    b'1lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmut'
    b'tdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lpr'
    b'rbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY6'
    b'2plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8A'
    b'AAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAA'
    b'AIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAz'
    b'FQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAA'
    b'AAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg'
    b'2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUA'
    b'AAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAA'
    b'AAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZT'
    b'tdZaa6211lprrbXWWmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lpr'
    b'rbXWWmuttdZaa6211jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZa'
    b'a6211lprrbXWOtqZXwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXW'
    b'WmuttdY62plfAAAAAAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa621'
    b'1jramV8AAAAAAACA4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZ'
    b'XwAAAAAAAIDgMxUAAAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62plfAAAA'
    b'AAAAgOAzFQAAAAAAACDYTAUAAAAAAAAINlO11lprrbXWWmuttdZaa6211jramV8AAAAAAACA'
    b'4DMVAAAAAAAAINhMBQAAAAAAAAg2U7XWWmuttdZaa6211lprrbXWOtqZXwAAAAAAAIDgMxUA'
    b'AAAAAAAg2EwFAAAAAAAACDZTtdZaa6211lprrbXWWmuttdY62pnfD3t3UAMAAAMhzL9rDCCh'
    b'feFhyQ4AAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vz'
    b'CwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAA'
    b'AAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAM'
    b'x1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAA'
    b'AAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAA'
    b'YNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYC'
    b'AAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAA'
    b'AACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNm'
    b'qtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa621'
    b'1lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXW'
    b'WmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZa'
    b'a6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lpr'
    b'rfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqb'
    b'XwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAA'
    b'AAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABg'
    b'OKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEA'
    b'AAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAA'
    b'AMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMV'
    b'AAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAA'
    b'AAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2'
    b'U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmut'
    b'tdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa621'
    b'1lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXW'
    b'WmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZa'
    b'a62nvfkFAFJ7iq4AACAASURBVAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXW'
    b'WmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZa'
    b'a6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lpr'
    b'rfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqb'
    b'XwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAA'
    b'AAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABg'
    b'OKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEA'
    b'AAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAA'
    b'AMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMV'
    b'AAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAA'
    b'AAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2'
    b'U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmut'
    b'tdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa621'
    b'1lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXW'
    b'WmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZa'
    b'a62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe'
    b'/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAA'
    b'AAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAA'
    b'wzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoA'
    b'AAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAA'
    b'ABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJup'
    b'AAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAA'
    b'AACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCw'
    b'maq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1Vpr'
    b'rbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmut'
    b'tdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa621'
    b'1lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXW'
    b'Wms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ72'
    b'5hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAA'
    b'AAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAA'
    b'GI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QA'
    b'AAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAA'
    b'AMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhM'
    b'BQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAA'
    b'AAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACG'
    b'zVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZa'
    b'a6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lpr'
    b'rbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmut'
    b'tdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa621'
    b'1lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0'
    b'N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAA'
    b'AAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAA'
    b'wHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYC'
    b'AAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAA'
    b'AACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNm'
    b'KgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAA'
    b'AAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAw'
    b'bKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XW'
    b'WmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZa'
    b'a6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lpr'
    b'rbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmut'
    b'tdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62n'
    b'vfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIA'
    b'AAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAA'
    b'AIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEV'
    b'AAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAA'
    b'AAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2'
    b'UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAA'
    b'AAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACA'
    b'YTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq1'
    b'1lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXW'
    b'WmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZa'
    b'a6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lpr'
    b'rbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms9'
    b'7c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcA'
    b'AAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAA'
    b'ADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6p'
    b'AAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAA'
    b'AACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCw'
    b'mQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAA'
    b'AAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAA'
    b'DJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSt'
    b'tdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa621'
    b'1lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXW'
    b'WmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZa'
    b'a6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrr'
    b'aW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78A'
    b'AAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAA'
    b'AIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBM'
    b'BQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAA'
    b'AAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACG'
    b'zVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAA'
    b'AAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAA'
    b'YNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZq'
    b'rbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmut'
    b'tdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa621'
    b'1lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXW'
    b'WmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZa'
    b'T3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkF'
    b'AAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAA'
    b'AAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZj'
    b'KgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAA'
    b'AAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAw'
    b'bKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEA'
    b'AAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAA'
    b'AMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNV'
    b'a6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lpr'
    b'rbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmut'
    b'tdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa621'
    b'1lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXW'
    b'etqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0v'
    b'AAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAA'
    b'AABgOKYCAAAAAAAADJupQO3dQQ0AAAyEMP+uMYCE9oWHJTsAAAAAAACGzVSttdZaa6211lpr'
    b'rbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmut'
    b'tdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62n'
    b'vfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIA'
    b'AAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAA'
    b'AIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEV'
    b'AAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAA'
    b'AAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2'
    b'UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAA'
    b'AAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACA'
    b'YTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq1'
    b'1lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXW'
    b'WmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZa'
    b'a6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lpr'
    b'rbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms9'
    b'7c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcA'
    b'AAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAA'
    b'ADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6p'
    b'AAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAA'
    b'AACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCw'
    b'mQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAA'
    b'AAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAA'
    b'DJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSt'
    b'tdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa621'
    b'1lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXW'
    b'WmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZa'
    b'a6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrr'
    b'aW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78A'
    b'AAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAA'
    b'AIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBM'
    b'BQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAA'
    b'AAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACG'
    b'zVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAA'
    b'AAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAA'
    b'YNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZq'
    b'rbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmut'
    b'tdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa621'
    b'1lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXW'
    b'WmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZa'
    b'T3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkF'
    b'AAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAA'
    b'AAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZj'
    b'KgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAA'
    b'AAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAw'
    b'bKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEA'
    b'AAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAA'
    b'AMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNV'
    b'a6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lpr'
    b'rbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmut'
    b'tdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa621'
    b'1lprZX1MOAAABKBJREFUrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmut'
    b'tdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa621'
    b'1lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXW'
    b'WmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZa'
    b'T3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkF'
    b'AAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAA'
    b'AAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZj'
    b'KgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa6211lprrfW0N78AAAAAAAAAwzEVAAAA'
    b'AAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXWetqbXwAAAAAAAIDhmAoAAAAAAAAw'
    b'bKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0vAAAAAAAAwHBMBQAAAAAAABg2UwEA'
    b'AAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAAAABgOKYCAAAAAAAADJupAAAAAAAA'
    b'AMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAcUwEAAAAAAACGzVQAAAAAAACAYTNV'
    b'a6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAAAAAAAMNmKgAAAAAAAMCwmaq11lpr'
    b'rbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACAYTMVAAAAAAAAYNhM1VprrbXWWmut'
    b'tdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoAAAAAAAAwbKZqrbXWWmuttdZaa621'
    b'1lprrfW0N78AAAAAAAAAwzEVAAAAAAAAYNhMBQAAAAAAABg2U7XWWmuttdZaa6211lprrbXW'
    b'etqbXwAAAAAAAIDhmAoAAAAAAAAwbKYCAAAAAAAADJupWmuttdZaa6211lprrbXWWms97c0v'
    b'AAAAAAAAwHBMBQAAAAAAABg2UwEAAAAAAACGzVSttdZaa6211lprrbXWWmuttZ725hcAAAAA'
    b'AABgOKYCAAAAAAAADJupAAAAAAAAAMNmqtZaa6211lprrbXWWmuttdZaT3vzCwAAAAAAADAc'
    b'UwEAAAAAAACGzVQAAAAAAACAYTNVa6211lprrbXWWmuttdZaa62nvfkFAAAAAAAAGI6pAAAA'
    b'AAAAAMNmKgAAAAAAAMCwmaq11lprrbXWWmuttdZaa6211tPe/AIAAAAAAAAMx1QAAAAAAACA'
    b'YTMVAAAAAAAAYNhM1VprrbXWWmuttdZaa6211lrraW9+AQAAAAAAAIZjKgAAAAAAAMCwmQoA'
    b'AAAAAAAwApM9IcxQ55JxAAAAAElFTkSuQmCC')
index.append('Grapher_background')
catalog['Grapher_background'] = Grapher_background

#----------------------------------------------------------------------
hand_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAaRJREFUOI3FlL9LHUEQxz/PBCIWQopgypupLAQlJCEWIaVr'
    b'Y+GLFkpEDbG0tQqxVPwLUgQrf3SChTeBQLCxMlUsrHbTSCxUUBsTCGeRFd47705FwYFlh+/M'
    b'fHdmdndqWZZxl9Jyp2zXJTTRAxO9Vim1opJNtBtYAuqAAv3ANtAB/AGmgQ8u+O/52IclB60D'
    b'q8Ac8BR464Lfi1nuRsJ54GU+8FLJJtoOnLngZ4Bx4BXQ1uBSd8FvAGcm+u1KQhf8CfDTREdc'
    b'8McRHm5wucBeA1/zvS27lC+Ai/oa0Bv1PWDfRFvi4Qv5wKYemugs8Ax4HEnGXPCDJtoVXXpc'
    b'8P9MtLMh7GNVhp9c8APAO+CBiS7HTHbifhD9PPA86n1VhBMmuuyC/xUz7c6XFIn/uuB/mGgP'
    b'cNhkzLKsaaWJHKaJTOXxopUmspImMtSIFV1KF/DZRHsLbHl5A1hVybjgfwMvgC0TbS1jMtH3'
    b'wK4L/rSSMJJuAwvAZkV2o8DiJfSKHp2miTwqse0U4WV/+UImgU0TnQOeADXgiP9PpnD6FE6b'
    b'28j9DNibyDmbwuTQD6W51QAAAABJRU5ErkJggg==')
index.append('hand-click-trans')
catalog['hand-click-trans'] = hand_click_trans

#----------------------------------------------------------------------
hand_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAadJREFUOI3FlDFIHEEUhr+7BAwp0kmsLXYawUOixEJSOjYW'
    b'uZjCEDAJpsy+ThHElIrNtCnEKme6gEX2BQJyjZWpYuE0IY0kxZ2Q2GggbApHONfd9SQH+WHY'
    b'x//e++e9mZ1XSdOUXqLaU7VuBY1oy4h21Uolr2UjOgy8BerAIDAF7AF3gVPgFTDvnd3J5t4s'
    b'2GgbeAesAgPAI+/sYajyIAiuAWPZxEstG9E7wIl3dgGYA+4DtztC6t7ZD8CJEf10paB39hfw'
    b'xYjOemd/BvpxR8g5NwF8zJ5t0aVsADbY74HxYB8CP4xoNWy+XlqhEX1tRLeBJWA2JD0EFkNI'
    b'zTv7B4g60pbLKlzxzk4DT4EbRrQRRPfDtxXivgL3gj1ZJvjMiDa8s9+AEWA421IQ/u2d/WxE'
    b'a0D7gjNN0wsripN2FCcvs3zeiuJkK4qTmU4u71KGgDdGdDzHl8UDQMtaxjv7HRgFdo3orSIl'
    b'I/oCOPDOHpcKBtE9YB1ollT3BNi8xF5xRsdRnPQV+Pbz+KK3fI7nQNOIrgL9QAU44uyXyZ0+'
    b'udPmX/B/Bux18Bexd+cVCoPFZQAAAABJRU5ErkJggg==')
index.append('hand-hover-trans')
catalog['hand-hover-trans'] = hand_hover_trans

#----------------------------------------------------------------------
hand_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAUBJREFUOI3FlM0rRGEUh58ZwspslLCRUpJCbCR/wNgqC2Ul'
    b'lsrS2gZ/hhp2RDZKo1iI7HxlJSW7WWCl1GPzTt1m7sfQlFOnc/qde573nvd2T06lmZZvKu0X'
    b'QINnWi5h5FGgBMwBA0ARuAG6gS9gFVgGzuqP1jh/UbfUA/VS7Qu66qM6q17H9cbBOtWnkBcC'
    b'ZDACHA75uXpa2x93hx/ALbAAvAdtPlKvajPASd3dJoxcVHdCvq8eh/xVbVHz4W2JxNiRS+qR'
    b'eqF+R/SRELtCHIqADtOA1Yf6Q76bMEGbOhHyShpwIwIZV+8TgFUfUx+yvnJFXckAVX1PXcsC'
    b'9oRxpxoAvqm9WUDUyQDtSIEtqeVaPe30bfUqpV5WF38DRP1U2xNqd3F6a8byWAeegU2gEPmT'
    b'poHeuIakbfNn+7cF27D9AEgV0o4edBUQAAAAAElFTkSuQmCC')
index.append('hand-normal-trans')
catalog['hand-normal-trans'] = hand_normal_trans

#----------------------------------------------------------------------
hide_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAPNJREFUOI3d0z9KQ0EQx/FPxEsIdgk+sEyffgsPkFwgqcQX'
    b'iKcwkBWr5ALxABavT59SWEk6wWPE5j3IXxF9hTjNwP7m9x12Zrex2WzUEWe1UP436PyUkOXF'
    b'0S2kGBrHzhv7W8vyYoEmLtDBupSaWOAD6xRD5yQoy4sHjPCI9xTDeK/JCJe4wzjFcH8AyvKi'
    b'jylmKYbBqSuXtVP0MUgxzNgd9lOZb7+C7NVUnh3QdZlfvwGqairPwYy6mGOJtxRDL8uLNqQY'
    b'lllezHGFNnophuejoBI2QQs3GGJVSi1M8IJVimG47TsAbQF/945+Gn/vr9UG+gThrlgHjd+z'
    b'/gAAAABJRU5ErkJggg==')
index.append('hide-hover-trans')
catalog['hide-hover-trans'] = hide_hover_trans

#----------------------------------------------------------------------
hide_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAMpJREFUOI3dkzEOgkAQRR/GyB2srShtrPAcnMATeAsaWk6g'
    b'B/AEWlnQWllzB2zGwi+ZbBaMCYXxJxPIn7fDZHZIzIwpNJukyn8Xmo/khm4hiZmxji5Aq/cc'
    b'WCpyea2Y4LNmPkp7qTKzfZBDXiWm9DkP7QTUkQJh1GJ3by9xC9kBCyAFHiOzQ1wnLg1nlOl5'
    b'+1DEM1nvBC0Xarkxs4O8tQJ5jZjCnw2v/whsgBVQAFfgrtxW3gk4i+3lZxTqqz0aW8jogSH9'
    b'3r82WaEnTyLLPmnrEUcAAAAASUVORK5CYII=')
index.append('hide-normal-trans')
catalog['hide-normal-trans'] = hide_normal_trans

#----------------------------------------------------------------------
input_1_file = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAX1JREFUOI3F1L1qVFEUBeBvz4SAhWgQkaksY5NSEQsRsdRC'
    b'W9HW0kIs8g5WIljE1Da+QgQHfAXLCAqKMRo0qAk6WRZ3lDG5VyekcMGBc/fPunvtc/bhfyPJ'
    b'X/21O7iqJLmEWxgh47gZ3K+qYZKqqlbm3h/sDdlp3MMXfMYmPuIUniS5XFX5V6WTVX5LcrPF'
    b'vpRkMcmrJFe78nsttj42WuxDDHAdi0luJJmZpsKtJNfG+0py5Je8JFeSrCRZTYNj+yU8mmQh'
    b'SW/8LclcknNJ3iU5Po3kSZzAWczSHFpVbeATdtoSunrQT3KYzFN3sJbkOb7ih6bPrWgjDE7i'
    b'ITXAPJbxFC/wBlv7qbCwhiWcwUWs4BHeau7nQEe7uiRvVtWzJNvkMXW7qt7/lpAc6sjrPJTx'
    b'SOY1tayZlBb/dIQ9fB/nrWPV3n6NuojbJI8wB1W1jZctMbPjtWeg2wjPYynJBc0V2Y0dLOAu'
    b'Pux2Tvt8TaKPYVU9aPnZwTD1E3YQ/ATpD8mE0kfUZwAAAABJRU5ErkJggg==')
index.append('input-1-file')
catalog['input-1-file'] = input_1_file

#----------------------------------------------------------------------
input_2_live = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAaFJREFUOI3tkDFvE0EQhd+ak+hoQEgULihcpLKo8y+Q6FLD'
    b'f4AWpYj4DdQnuUiDKJCMLBdQoEhusEVcIBp8J3zXeG9v53ZmhyIcWDiJbWgoeNXuzLxPbwb4'
    b'r3VZa6/976wsywAAqmqccykRuaqqDv8KCgBN07zQH2Lmj3Vd3/lzGgAiOm+BMUYVkYNtnuS6'
    b'pqpS+zbGRGOMbgN2fi9Mp1NMJpO2btZnVVXG4/GN2Wy24bsyYbfbvQngcZ7nMwB+rVUR0b1+'
    b'v3/U6XReAfiwLS0AQFVvxRg/13V9QkRn+ksr59wjEVFVfXKVfyN60zQaY3RJknwzxrxRvThb'
    b'jPG8qqpPxhiIyE7hAADL5TIhomMRyReLxX3v/bMQwsuiKA6YOY0xFmVZ9nYnArDW3mXm18xc'
    b'hRBOmqZ5zsxnIlJ47x8CADPvBmtXdM7dDiEcMfM7EXEhhGMietDOzOfzS/0bNxwMBgCAuq5N'
    b'WZZvmXmoql9Xq9WptbYEgNFohF5vv61hrX0aQvgiIpmq5sycee/f70cBkKbpz7Uvk6piOBzu'
    b'zf139B3UYzEy01Hv0QAAAABJRU5ErkJggg==')
index.append('input-2-live')
catalog['input-2-live'] = input_2_live

#----------------------------------------------------------------------
input_3_mic = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAdZJREFUOI3tk7GKU0EUhv+5ernsRgRFEpAQELcRLASxTO8T'
    b'WO8TWPgEClpa+Ah2IYVsE1AkxkKIhiBWCSGwsViXG8K9psjNTObMmWNhsmSvkc2KhYV/N/xn'
    b'vvMfzgzwX39NcRwDALTW17TWn7XW/SzLigAwm83+HExEr2Qpa+2bvC8i28Pa7faOtXaxAnrv'
    b'rTFmdwN0V0QeiEiU94JcoQJgVmellI6i03dE5AqAIwD7AC5sBPZ6PdXtdoPpdMq5JoG1lhuN'
    b'RtDv99WyyXcA9wD0Aag88CIAVCqV6977/VKp9FpEZgAuLf2ZMeZ2tVq9r5R6uUwGADv56U4B'
    b'C4VCWUSeeO9HQRD49YIwDG9FUfQ4CIK3a8DfKgAAa60TEROG4RGA9yvTOffJWvtVKeWYOX/v'
    b'l4WcKI7jy0T0jpm/DAaD4mKxeG6tfTEajYrM/NE59yFJkqvAFs/GmJ9LzbLsDjP3nXNjInpG'
    b'RE+Z+RszD7XWd5eJz5oY6HQ6J12NMTeI6CEzj5xzh865R1rrm6tkw+HwbCAA1Ot1AECSJOU0'
    b'TfeI6MBaezCZTPbSNC0DQKvV2g62rvl8XieiY+/92Hs/JqJjY0z93KBarbb6JRslIqrZbJ4/'
    b'4T+pH1BnLU0zFEo/AAAAAElFTkSuQmCC')
index.append('input-3-mic')
catalog['input-3-mic'] = input_3_mic

#----------------------------------------------------------------------
input_4_mic_recirc = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAA7BJREFUOI11VE1oXFUY/V4nVuiEqSZGyEhciVjrRiwSFaVg'
    b'mkUjKOhSd3Gj4Erwh1YEBUGE+EeysBvjopsu3IiUNhEak2YwExJJJmSSCZOZyUySeTNv3nv1'
    b'vXd/vntcdF6ZaZqzu98953zn3u9yiR6AxcXFrvXs7KwVBIE1NjZmxTUAND4+fkRr3V9oNpvU'
    b'19dHRET1ev0ZpdTTyWTyqWQyaSqVihkaGro5MzNTGR0d9R4UpgvZbJaIiIrF4mnHcX6WUua1'
    b'1mBmGGMgpQQzlz3Pu1Gv188REW1tbR0J1YWVlZVXwzAsAYBSCrZt/9FoNN4HcLZarV7SWi8Y'
    b'Y8DMbqFQ+KEdoNtkYWGBiIiGh4ctIcQ2ADQajX8KhcJz7fuygiB4NOa7rvupMcaWUqJUKn1+'
    b'bDrbtq8CgOu6fy8tLQ0SEUkpT0gpP5RSIoqi12KuUuoFZv4PgG3b9vARs2Kx+KKU0gVQz+fz'
    b'A+1kJKVMaa03AICZb8V8AJ8dHBz8yswIguArY8wlAI/cM6zVaj8aY9BqtX6PzYiIwjA8rZQq'
    b'4i4ynSGMMTVjDADA87zvc7ncSero+BMAAeB8XGu1Wid9339MKbXTNrxNROQ4Tk9bM26MYSHE'
    b'TDab7es6MoABAGcA9MY1IcSXrut+opRaaRte933/4yiK3o051Wr17dXV1SeJiMrl8t2HzcyU'
    b'SCQ6zS3LssDMGWNMnoj6enp6LjLzFSLqTyQSFcuyPqrVatbg4CBiXSaTIUqn051GOQDr8ToM'
    b'ww+YeTcIgotKqV983x9m5loURW/GnN3d3bHNzc1/5+bmXu488alms/lXfMHGmD/joSilrjLz'
    b'tpTyC2a+I6X8tlNo23ZZCIFyufxWZ7LX9/f3L0spm0KIoNls/tY5HKXUZWb2oyh6p80nIqL1'
    b'9fUzQggwc9bzvDR1bhIRaa2njDFwXfe7uOZ53gWl1C1mdoUQ13zff56IaHJystdxnHkAcBzn'
    b'SteE5+fniYhoYmIiFQQBlFLY2dn5pp3upFLqcQADUsoBAInp6elUo9G4zswAUFxbWxu6PxxN'
    b'TU3FiZ8FcEcpBQBfVyqV8wBOAUgB6K3X629ora8xM4QQ0d7e3ntERKVSiY4g7hAEwUtCiCWt'
    b'NaSUMMbkAeSNMdtKKWitEYbhzcPDw3NERAcHB/e+sGP/so2NjSfS6fQrAC6kUqmzlmWxMeaE'
    b'67oZIrqxvLx8e2RkpNVoNKi/v/84m/bj7EAul3tYa90LICmlTGYymYeOVxP9D9eYAXHWaByG'
    b'AAAAAElFTkSuQmCC')
index.append('input-4-mic-recirc')
catalog['input-4-mic-recirc'] = input_4_mic_recirc

#----------------------------------------------------------------------
knob_disab_sm = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAACHVJREFUWIXNmF1oHNcVx393ZnZ2V155vbuWV/JHFIGsVNgE'
    b'Q0MDFpgQtxBoCa7dgChpEhrSUGhIoS15SNO0zYMfamOSvrWlcZM0dkNpFUFIHduidoQxcqza'
    b'hbW1+haSN5UiRbvS2tr5vH3QzGo0kh2llqEHDju7O3PnN/97z51zjpBS8v9synoP+NBDD726'
    b'nuOtCVAsmSKE2CuE+KYQQhdCRIUQcSFEjecbpJT7hRAJIcSGwO9x71xdCBERQqjeWEIIIe4K'
    b'0BtAeOeqQA3wDBABdM+jQMxzK/TdP+4ADgKa56o35h0htTWA+e4P+C/AAR4BegK/K4BwHGcE'
    b'2ABIz12gBWgCTnsP5Hjuep9SCCEBKUNBIVYLkhCcr5waePq2w4cP721razsohNjpui6O41Td'
    b'/+66LqZpDh47dqzvwoULvcDvAdtT2fY8CLsCcgVgCG4f8BXgHQ9MP3v27FPJZPIH0Wi02XVd'
    b'bNvGsixs28ZxHGzbXgZo2za2bVMul4fGx8ePv/zyy+8CpgdprgK6DHI1QCWg3APAq8C/T58+'
    b'XdmyZctz8Xh8pxACx3EwDIOBgQEKhQKzs7NYloUQAl3X2bRpE+l0mkQigWVZWJZFpVKhXC4P'
    b'jY2NHT9y5Mg73qy8AxwCZj1Q1wN0VwB66vnrSWMxEOqz2eypDz744P5MJgNAsVjk/PnzjIyM'
    b'YFkWtbW1pFIpamtrURSFcrlMqVSiWCwSjUZpbGwkmUxiGAaGYWDbNl1dXa93dnZ+FfgH8Adg'
    b'ITD1LuBKKaUWggsGhAZEurq6Hq+vr78/Fovhui49PT10d3eTSCTYvXs3dXV1RKNRVFUlEomg'
    b'qiqapqFpGkIIxsbGuHLlCoODg7S2tmLbNqZp0tDQ8GJra2vn9evXTwbEkAEXQoglBQPq+YGg'
    b'f/TRR9/PZrNH4vG4/9Tk83mam5tpaGhA1/VlYGHAIOjg4CDnzp2jqamJcrmMZVm4rks+n//l'
    b'yZMn3/YUrITWpRvcB8PTqyeTyec1TcOyLM6ePcv169fZvXs32WyWL9hfl5mqquzatYtDhw7R'
    b'399PTU1NNbh27NjxNEv7pe7du7pthQG/C7wHtL/55pvP67q+03VdLl26RD6fp7W1lQ0bNqwZ'
    b'LGzbtm2jvb2diYkJ0uk0juOgqmrTgQMH2oGkd//fEtjEw4AdwBvA1y5evPiCEIJSqURPTw/b'
    b't28nkUj8z3C+NTY2sm/fPsbGxohEIliWRUNDw1PAKWAv8OfbASoszvvlzs7OvmeffXaz67pc'
    b'uHCBWCxGOp2+azjf9uzZU418x3GIx+ON+/fvfwv4OZALACqrrUG1pqbmOSklpmkyPj5ONptF'
    b'UdYv8YlEIrS1tTE1NYWUEtu22bVr13dYekffVkEFUIUQO23bpr+/H9u22bhx47rB+bZnzx7K'
    b'5TLZbBbHcdB1vYmVicSqCir+K2tiYoJ4PP6lInatpqoqmUwGXdeRUuI4DixPPBRAVDfqlpaW'
    b'bZZlxS3LqrEsC1VVKZVKxGKxdYfzraGhgdnZ2WqSkUqltui6vjESiVQWFhbGZ2ZmjCpgIpH4'
    b'UyqVuk9KqRUKBRobG7FtG1VV7xlgKpViamoK27bRNI2WlpZfbNq06T7HcaxCofCzmZmZD6uA'
    b'vb2933jllVe+bhhGbV1d3due5NzLmsUf28+EyuXyrx5++OEmRVGmzpw5cw5CCetrr73WDdR0'
    b'dHT4m+g9BZyZmUHTtOoU53K5Yi6XOweU/XNW3Tv8CxKJBJVK5Z4BTk5OoqpqVUGWEoWqBQGr'
    b'mYQfxZlMBsMwcF133eFM02RmZoZisYhpmmHAqocVlID7+eefD1cqFVKpFJqmMTc3t+6AuVyO'
    b'2tpacrkclmUxMTFRYLEgc1lK/1co+ADw05deeik6OjqKYRik02kmJyfXVUXTNKs55cLCAl5C'
    b'UgCOAT9ksehyCSnoAt8GSqVS6UAqlRqqVCqk02kMw2B6enrdAC9fvszc3ByXLl3y65mxubm5'
    b'F4CfsJQ0u4TyQQn8msV05z9DQ0PHDcPANE3q6+u5ceMG8/Pzdw03PDxMd3c3mqbx2Wef+Vn3'
    b'eyym+wXgKDDNbRT061T76NGj75bL5SHDMABIp9Ncu3btrtbjyMgIJ06cIJFIcP78eWzbBhjr'
    b'6+v7G0uVnl/hraqgD2gB5vDw8HGvtkVKSSaT4dq1a9y4ccOPujWZaZpcvHiR999/n82bN3Pq'
    b'1Klq8fTpp5/+xYPz3QoAymBN4hfoGoupdwyIP/rooz/esWPHi9lsFikl0WiU2dlZYrEYzc3N'
    b'bN269bZFEyxO6dWrV7l58yZCCD7++GNM0yQej9Pb21uwbfuPwAngFivrEueORROwFTjc3Nws'
    b'n3jiiccNw8BxHBRFIR6Pc/PmTQzDIJFIkEwmSSaTKIrC/Pw8xWKRubk5ampqiMfjfPLJJ0xP'
    b'T/sJKoVC4Tejo6P/BF4Aulisj1cUTWHAIGQEOMNi3frWwYMHn9y+ffvTiqI0WZaF4zhIKUkm'
    b'k0QiEVzXRUqJlLJayZVKJfL5PAsLC9i2jaIoCCHGJicnTw4MDPzVA8oABjAQWofLpzikog+Z'
    b'8taD5k159LHHHmtvamp6UgjR5Lc5/FZHsP3h17+WZSGlxHXdsYmJiff6+/v/7gFVQp9hOFdK'
    b'Kb+o9eEr6bfaop7re/fufSYSiXzvwQcfrAs2jsJNpFu3bo3m8/mOvr6+duBbgWAwQmDLlFu1'
    b'9RGaar/DEOxq6QHYdhbfPMcI1BCew/L2mwu8zmLV2MGXaB6t6A9KKWUgxa9eELiRP+AjHtw8'
    b'y9P0oLkBfwN4HniXu2m/3UbJYAPTV/VHwO8INTDvoKAPEYYKirC2BuYdQJU7eBDOtzDkar4q'
    b'2JoBA5CEQMPHwf+DcP6xy3Lg6v+3gwP4L297s8Cw4xrlAAAAAElFTkSuQmCC')
index.append('knob-disab-sm')
catalog['knob-disab-sm'] = knob_disab_sm

#----------------------------------------------------------------------
knob_trans_sm = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAACEVJREFUWIXNmGtsHFcVx393XruzXsd2/G7tpIbEpapUIRFR'
    b'KZFQ1YBUCVSFQKUIlbYiKhUSVZEA9UMpBfohH0gUtXwDRENbSqgQuJZCH0lMyyOKSGr6MnUe'
    b'TuzY3SSt147ttXdn5s69fNiZ9XjspClxJI50tLOzs3d+8z/33jnnCK01/89mrPaAmzZtemI1'
    b'x7sqQLFohhBisxDiy0IIRwiREUK4Qohc5HVa661CiLwQoi5x3o2udYQQthDCjMYSQghxTYDR'
    b'ACK61gRywAOADTiRZ4Bs5EHqe3zcB2wHrMjNaMwrQlpXARZ7POC/gRC4A/hX4rwBiDAMzwJ1'
    b'gI5cAb1AD3AweqAwchV9aiGEBrROLQqx0iJJwcXKmYmn37Jr167NW7Zs2S6E2KiUIgzDmsff'
    b'lVL4vn967969w0eOHBkEfgXISGUZeRJ2GeQywBTcF4DPAM9HYM7hw4fva2ho+HYmk9mglEJK'
    b'SRAESCkJwxAp5RJAKSVSSkql0sj4+Pi+xx577AXAjyD9FUCXQK4EaCSUuxl4Anjn4MGDlba2'
    b'tgdd190ohCAMQzzP46233mPs3DgzMzPIUFbngmVTv2YN7a0t3NDZShAEBEFApVKhVCqNjI2N'
    b'7du9e/fzUVSeB74GTEegKgJUywAj9eL5ZFFdCB3t7e2vHjhw4Kbm5mYAisUpXn7lIIUPxlEq'
    b'xLSyWI6LZWUQhiCUPjKoIIMypmnT0trBuq4OlJJ4noeUkoGBgaf6+/s/B7wC/BooJ0KvAKW1'
    b'1lYKLrkgLMAeGBi4u6Oj46ZsNotSioG//p3jx45imA6ZfBuOk8cwLQzTxDAMDMOM3EAYgsr8'
    b'NFNTBT68MEH3uh5yroXv+3R2dj5yyy239L///vv7E2LohAshxKKCCfXiheC89tpr32pvb9/t'
    b'ui5SSl7q/wujZ0ew3SbsbD2mYS0CrQBYPWcihGBhbpLihdOsbe0glxEEQYBSihMnTvxk//79'
    b'z0UKVlLzUiX3wXR4nYaGhocsyyIIAvpeOsDZs6exc62Ydl10+dWZEAb1jZ3ccNNnmbw4wXw5'
    b'rC2u7u7u+1ncL53o3rVtKw34DeBFYMczzzzzkOM4G5VSvP63fzI6egYr24ww7KsGS1s210jX'
    b'pzZxafojNA5hGGKaZs+2bdt2AA3R/X9BYhNPA/YBTwOfP3r06MNCCKamp3n7rTcx7Pw1wcWW'
    b'y6+lpWMjxeJFwCAIAjo7O+8DXgU2A7+7HKBBNe5v9vf3D+/cubNFKcXhw6+DsBBm5prhYmts'
    b'7sK2s2BUVXRdd/3WrVufBX4EDCUAjZXmoJnL5R7UWuP7PhcvnEeYLp9kzn2cGYZJS8enmS/N'
    b'oLVGSsmtt976dRbf0ZdV0ABMIcRGKSVvv/MeWiswnFWDi62xuQsZeDiZPGEY4jhOD8sTiRUV'
    b'NOJX1rlz4yDMVYeD6sp2MnUgDLTWhGEISxMPAxC1jbq3t/fGIAjcIAhyQRBgmiazs7PXDRDA'
    b'rWsg8Mq1JKOpqanNcZw1tm1XyuXyeLFY9GqA+Xz+t01NTeu01lahUGD9+vXxU103s50cXmUO'
    b'KSWWZdHb2/vjxsbGdWEYBoVC4YfFYvHlGuDg4OCXHn/88S96nlff2tr63PWGq5pGa2qZUKlU'
    b'+untt9/eYxjGh4cOHXoDUgnrk08++Q8g19fXRxiGGIYB1xHU9+YxDLMW4qGhoUtDQ0NvAKX4'
    b'mhVT/vgPdfk86OsHWFmYAxYVZDFRqFkSsJZJxKu4rbUlAlz90lSpEM+bZ2F+Ht/304A1Tyuo'
    b'ATU1NXWmUqnQ2dGGEAYof9UBZ6cL2HaGwgdnCYKAiYmJAtWCTLGY/i9T8GbgB48++mhmdHQU'
    b'z/PI1zegwzKrqaJSIR9dOI0wbMrlMkopjh07VgD2At+hWnQpUgoq4KvAzMzMzLampqaRSqVC'
    b'140doEO0rKwa4PTkOQK/wulT/4nrmbHZ2dmHge+zmDQrUvmgBn5GNd25MDIysq+angc0rW1B'
    b'yRJ6FUI9PzfJ5IXTVDzJpekphBCMjY29SDXdLwB7gEkuo2Bcp8o9e/a8UCqVRjzPo87NkKur'
    b'R1aKqPB/h1woFZk4cxyNxdC7g0gpAcaGh4f/xGKlF1d4KyoYAwaAf+bMmX1RbUs+l8HN1SPL'
    b'k0h/Dj5B00kpyfRHo5wfexsMl8HjR2rF0/nz5/8QwcUeJAB1siaJC3SLauqdBdw777zze93d'
    b'3Y+0t7ejtSaQUF6YQxg2mdxanOwazCsUTeVSkdnpAmHgMV/2GXp3EN/3cV2XwcHBgpTyN8Dv'
    b'gQWW1yXhFYsm4AZg14YNG/Q999xzt+d5hGGI1qAwkL6H1iGG6WDZLpadRQhBKL2o7KxgWg5K'
    b'G5w6OcTMpek4QaVQKPx8dHT0deBhYIBqfbysaEoDJiFt4BDVuvXZ7du339vV1XW/YRg9QRBE'
    b'oBrLzkbCK9AajUAIgQIWSnOcL5yjXC4jpayqKsTYxYsX9586deqPEVAz4AGnUvNwaYhTKsaQ'
    b'TdF8sKKQZ+66664dPT099woheuI2R9zqSLY/pJT4vk8QBGitUUqNTUxMvHjy5Mk/R0CV1Gca'
    b'Tmmt9ce1PmIl41ZbJnJn8+bND9i2/c3bbrutNdk4SjeRFhYWRk+cONE3PDy8A/hKYjF4KbAl'
    b'yq3Y+kiFOu4wJLtaTgJ2B9U3z14SNQSLxUuy/aaAp6hWjX18gubRsv6g1lon+om1PyRuFA94'
    b'RwQ3x9I0PWkq4U8DDwEvcC3tt8somWxgxqp+F/glqQbmFRSMIdJQSRGuroF5BVDjCp6Eiy0N'
    b'uZKvCHbVgAlIUqDp4+TvSbj4WLEUuPb7kpCm2tX/BV0HrAK/xpabAAAAAElFTkSuQmCC')
index.append('knob-trans-sm')
catalog['knob-trans-sm'] = knob_trans_sm

#----------------------------------------------------------------------
load_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAMtJREFUOI3tlLEKwjAQhr9IERUFB5/Byd0nSWdXB8HnSgZf'
    b'QHTt6ubm5C6Cg1g8l9SmtKEKHSp405+78PHfHYkSEZqMTqO0nwBG/kHFdgVMA3c3YvSuDqiy'
    b'pajYzoA5MACern4HUqcPwMnpmxj9qAMegQTok4+iF9ApMALWYnTiA/2Wz2L0oq6lt5PYbl0H'
    b'hfCX0v0UljHJR1MJ/DaGwLVJoAJKz6xVDqFihv6WJyq2e6fHAYCfj6hw6AOXnr4EgIW8GF1y'
    b'qP7fV/uAL0qsNUpB0my9AAAAAElFTkSuQmCC')
index.append('load-hover-trans')
catalog['load-hover-trans'] = load_hover_trans

#----------------------------------------------------------------------
load_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAFtJREFUOI1j/P//PwM1ARNVTRs1kJeBgeE/AcxBioE5DAwM'
    b'ExkYGBhx4CoGBoYOQgYyIiUbctIPI7oACyEFeABWBwytWB4hBqLHMsVFD7KBpCQZnGDwh+Hg'
    b'NxAALDMTOXtBqyUAAAAASUVORK5CYII=')
index.append('load-normal-trans')
catalog['load-normal-trans'] = load_normal_trans

#----------------------------------------------------------------------
Mario1 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAA3NCSVQICAjb4U/gAAAADFBM'
    b'VEUBAAD4OACsfAD/pECFmYJ4AAAAAXRSTlMAQObYZgAAAE9JREFUGJVdjlsOADEIAkXuf+da'
    b'fKWdZD+YLgazC4QNGEp4QDptcgTqW/EYFSIHXWKxJx3o5/oX1+hItUGpFDPMqrZDU+ATeTF9'
    b'i9mzOzYdr7MBOykYeJMAAAAASUVORK5CYII=')
index.append('Mario1')
catalog['Mario1'] = Mario1

#----------------------------------------------------------------------
Mario2 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAAwAAAAQCAMAAAAVv241AAAAA3NCSVQICAjb4U/gAAAADFBM'
    b'VEUBAAD4OACsfAD/pECFmYJ4AAAAAXRSTlMAQObYZgAAAElJREFUCJlVTgEOACEIQvn/n4/A'
    b's8VqgwIUQBkwaiHRAtmEuQh9I1bZJC4cIwcJdc2zy7oqKpw69yczj0PpWUhqeZb765J6ys0+'
    b'd4kBE9uuw3cAAAAASUVORK5CYII=')
index.append('Mario2')
catalog['Mario2'] = Mario2

#----------------------------------------------------------------------
Mario3 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAPCAMAAADjyg5GAAAAA3NCSVQICAjb4U/gAAAADFBM'
    b'VEUBAAD4OACsfAD/pECFmYJ4AAAAAXRSTlMAQObYZgAAAEVJREFUCJlljosKACAIA+f2///c'
    b'sPWig6TDKQKmGoTatNJIFGL+qt/SyztqMzOugL2KxejMMaOuFU30PeK+6WtmNw5cPgCA2wEW'
    b'cesrCwAAAABJRU5ErkJggg==')
index.append('Mario3')
catalog['Mario3'] = Mario3

#----------------------------------------------------------------------
Mario4 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAA3NCSVQICAjb4U/gAAAADFBM'
    b'VEUBAAD4OAD/pECsfAB81QrqAAAAAXRSTlMAQObYZgAAAFFJREFUGJVlj1sOACEMAoHe/87b'
    b'1j7MOokfTNAgEDBBwaENZJI5HRXCT5nOIxBlpbruJFjMSKtnT5dHRC2yR7FeivpMQ4nf1Ftw'
    b'RX5pl+zCN3+wAgFJZUDctAAAAABJRU5ErkJggg==')
index.append('Mario4')
catalog['Mario4'] = Mario4

#----------------------------------------------------------------------
Mario5 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAAwAAAAQCAMAAAAVv241AAAAA3NCSVQICAjb4U/gAAAADFBM'
    b'VEUBAAD4OAD/pECsfAB81QrqAAAAAXRSTlMAQObYZgAAAElJREFUCJlFjgEOADEIwgD//+cD'
    b'nSfJknZTJ+Cwc7QGlVROUBEf23ILUqDWV9fBxJechzDDU0ZqbH+tkx72L2R562QYj7fjHPgA'
    b'edMBLXH5xvAAAAAASUVORK5CYII=')
index.append('Mario5')
catalog['Mario5'] = Mario5

#----------------------------------------------------------------------
Mario6 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAPCAMAAADjyg5GAAAAA3NCSVQICAjb4U/gAAAADFBM'
    b'VEUBAAD4OAD/pECsfAB81QrqAAAAAXRSTlMAQObYZgAAAEhJREFUCJltjoEKQCEIA+f2//+c'
    b'mksevIOgy7UCkmiA3a+DIpVcYWmudtsoKsY+eOnGTVToU6V7w9MinJ9fOB7P8TfG9I7uMweB'
    b'BgEmBijSmQAAAABJRU5ErkJggg==')
index.append('Mario6')
catalog['Mario6'] = Mario6

#----------------------------------------------------------------------
midi_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAktJREFUWIXtls1LlUEUhx9FSEhIqlUlzZk/wBYRRES2nCA0'
    b'sHIjJhG0NKgWBe0KhHDRMoLU2gWCLWqmWpTVrk21rpnCICQLC9tIMC3euXCRqzHvyzUX9wcD'
    b'83EO52HmMOe0xRjZzGr/3wD/UguwqlqAVdVRxdmJ7gbOAEeBI0A3sAS8BOaAKRP8UpUYpW/Q'
    b'iR4APgAjwHNgH7AdOAS8As4DH53oE1UA28r8g070BaA2HpvgV5zoLhP8cp1NB8XtXgfGTfC3'
    b'ShHGGLOGVTJqlfyySnpX7e+1Sh41sD9glSxaJaO5sWKMeU+ccm4cGDLBv29g0rl6wwT/BrgC'
    b'TCT/LOXm4AjwxQRvG5z9Bj6t4TcJfKd48izlAg6kYDjRyolWtQMT/CJwuZGTCf4PMJ38mwp4'
    b'FJh1oruAS2ldD/Kjfu1E33SiT6alBfqaDdgOLFDkWi/Fk6+n/cCNlHufc+FqAXMUgZ70nK8p'
    b'8m49dQLfAAXsyqYjH/AFMAhggr8KTKxlmP7B0yb4wyb4t8AwRXVpKuAsMOxEb0nrSSd6fg3b'
    b'eeBZgt0K9Cf/pgJOA7uBWvm6D8wkiNtO9Dsn+lo6mwVcmg8DO4GpXMDsUudEj1CUr3Mm+Kd1'
    b'+zMUdXgBOA50UTQOB4E7wEUT/L1cwOzSk8rXmFWybJUMNjjbY5V0pPmQVbJilYyViRNjLNcs'
    b'pBvrB+6mG3sAPAG+Aj3AMeAUsAM4a4J/WCoIJbuZOshtFOWrL41aPziXxjTwE8AEv/GAG6FN'
    b'3/K3AKuqBVhVmx7wL+qmck+9L15FAAAAAElFTkSuQmCC')
index.append('midi-click-trans')
catalog['midi-click-trans'] = midi_click_trans

#----------------------------------------------------------------------
midi_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAkNJREFUWIXt1sFrVUcUx/FPRGjAYIN1JUrzF9RFEUSkI7iS'
    b'FpWr1k1QEaFLheqAQjdaQW7Joi4EETSpqxYddGOwLuzY7rqRrltQFGzQlBQiSAnExZ3AI5jI'
    b'zeOlWeQHs5iZczhfzjnMmb7Z2VkrWWv+b4D3aRWwW60Cdqu13ThXdR7EUezCZxjEFB4hYzTF'
    b'MNVNjCVnsKrzPvyJI3iIrdiAHfgVX+Gvqs77uwHsW8o7WNX5FObWvRTDf1WdB1IM0x02azXZ'
    b'/RaXUgzfLwtgVedjuIydKYY/Os4/xpUUw+fz7LdhHKdTDKNtAVuVuPTcJRzuhOtQ//yDFMPv'
    b'OIuR4t87QE2/PU8xjL/j7jWeLOB3A5OakrdSW8B9JZiqzkNVnYfmLlIMr3DmXU4phhmMFf+e'
    b'Au7CnarOAzhd9p0g/3Tuqzp/V9X5YNmOI/QacA0mNL32iabki+lTXCy997Qt3FzANprFllLO'
    b'3zR9t5j68RJD2NSaTnvAX3AAUgznMLKQYXkHv0wx7EwxPMawZrr0FPAOhqs6f1D2N6o6P1vA'
    b'9hkeFNh12Fv8W6ntLB7DN9iPH3ET6wvEVWzHrRTDhQLzpvgNYyNG2wIuZZIc0YyvEymGnzvO'
    b'b2vm8AS+wIDm47Ad1/B1iuGHngMWmJO4iKMphtvz7jbj7xTDTFXnw5osn1m2WdwBshfXNRn7'
    b'CffxAluwB4fwEY6nGO4uKUg3gAXyQ834CmXN/QdzWWOT0zP/Qj6/e/kBl0Mr/su/CtitVgG7'
    b'1YoHfAsYmcVv10YFFwAAAABJRU5ErkJggg==')
index.append('midi-hover-trans')
catalog['midi-hover-trans'] = midi_hover_trans

#----------------------------------------------------------------------
midi_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAfhJREFUWIXtlj1rlEEUhZ9o/AAFF00hJhJLKwVBBBvFIpAm'
    b'CajYhFUUsdwUWvoDxNbGxrikE2JiISpiRPQHaK8QjBA1CahoI4bH4r0Ly7K7ZnZYFNkDl/m6'
    b'h3uYuTN3+lT+ZWz62wL+hJ7AXPQE5iJXYAmoAHPAGrAe7RwwFetZyBE4DrwFysBz4DCwGzgO'
    b'vASuAO+AiSyFaic2pS6qE+rWmNvZ4NOvXlKX1UqHcToSeEH9ph5qmB9WHzbxP6quBq/rAkvq'
    b'R3W0ydqw+qwF77K6FvykmKk5WAY+AI+arP0AFlvwpikuz/nEeMkCxyMYwIGwGlaBay14v4Bq'
    b'8NOQuOXr6mBciFsbyKub6pnoHwl+Usw+034zAlso3rf7sTOn2vgvAIPAMWAz8DnaDSP1iAX2'
    b'UxznK4q8a4ftwApFKuxLjBUR07Z8Qb1aNz7ZxrdfHaob3wh+V2/xPDAJbIvxNLDUwncJeBr9'
    b'HcBY8JOQKrBKkVO18jUDzEb/NvAGuB7jeeBx9CeBAeBuqsDkl10tq+/VkYb5WYuy9jqO9qC6'
    b'16IcrgSv65WkZhX1u3q6ydpQ5B/qOfWnGbU49ZmpxxhwB/gE3AOeAMsUt3wUOAvsAS4CDzoN'
    b'kiMQYBdF+ToRVgK+AC/CqsDXnAC5AruO//7L33X0BOaiJzAXvwE8vKSep8MpcwAAAABJRU5E'
    b'rkJggg==')
index.append('midi-normal-trans')
catalog['midi-normal-trans'] = midi_normal_trans

#----------------------------------------------------------------------
next_24 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABipJREFUSImFleuP1Fcdxj/n/C4z85vbzszO7C67XJZ1QdYC'
    b'bbmWokJDWzXGW1+Y9B8wqW0lNV4SE0PVN9qmWpsmLbX2ggUiIrZpSrVKCNiWCqTI4roLLLAL'
    b'7M4ys7vs3C+/c44vRsrFNj7JyXn3fL55znnOETzOzdI37BYb0pHMfYtivSsTwUSfZ3lOWZWb'
    b's/7MubFjFwZzU7m/8A6HKfCJEv8D8AHJ5vXdG36wLrN+yzxvvqWVRmuN1gaNBgE6qMg2JvWx'
    b'00cOHP/jsV9wiHf+P0BhZcId27659MEf9keW2jOVWQq1Ag3dxKDRxqCMxmAQQDgQoS0WZ5zz'
    b'+vU/7X0qvzv3Y6ap3giw2PzR5M6iZO/LD6/Y+nBUJOTluQmqzQoK1TLHoIXGCI1Go4Sm4leY'
    b'rsySoF2sWr1qw3j32LLC0bm3aNC4Dvh8K5Z0NP2TR1c+9u1GzSdXzmPQKBRKa7QwlGtlCqUi'
    b'DdPAci2UaEG01BSaBWhIVg2sXjYih2LV49W3MdcAm0BKec+3Vjz0gmciIl+ZBgw+Cm0UCk25'
    b'XmF+YB5fWf5FdENxOn8WO+KihGpBLENJl7F8h8V39K0dPHPilLlohlqAz2Gv7V732sbMpp6J'
    b'wiRGtMyVaS1fKBrlOt+/fytrl6xmQ/96xrOXOJUfIhAPoi2DtgzGEhRVmXnhbqodxYGpv2Z3'
    b'o6hJ6ci7P9u1ad1MeRZtNEpfM9f4QqGkxpeaWrMOgG3ZfO9L32HTvI1cyk1QETWq1KlRoyEa'
    b'XC5OsmL56tvkHfI+AGv+Vxc8srnz3g35ynTr8Ggdoi99fPxWxqbI+2ePsHrBnSS8NixpcVfv'
    b'Go6c/Qd/GNlH1uS4VLrMRHmSC8WLeKEwc4V8pXqs8oa9MLpwja/81uT/Na/7DWqVKspoJiqT'
    b'TNSnyJcmmdqTZ9eDv6Ur1oFruzz3wK9gH7w6vpt4Mg5aUFc1JgtZEgPJlTN2vt1OBlPztDa0'
    b'7A0KjagavrvpEZZ099NUTaSQSEtSV3XagvGP7njAdtn+9acJvumyd+oNAtEQAd/BsW3cUDSN'
    b'JC61MGlf+yAECDg6doygG2JN/yriXoz2aIpkJEFbKE5HJEPADtzUVMd2eOL+n9Ep04Rcl0jQ'
    b'I2i7yIBMIPBsjJmVQsZ95XPownsMT52gVC4zMnmGRe0Lbiq9b5pY0iJoB2+C7Bnah4xAPBRB'
    b'KUU05FEsVCtotF1UxSnf+Iv+duYgo9OnIRxmtDnK+u1b6El1Iy2JY9ko7dMVyPDLLz9Bf6oP'
    b'A1gSdny4k+fOPk+qI4FEUPebJLwY0/WJHJqyfTE7/uH7paPrRqeGIRRqRRVyuRq4ytXmLBgH'
    b'SwvSjSTbNm6jt62PSkPjSsmOwV28PP4iXQvSOMJBG0NDNUhG40yP5EZQ5OWFd8/vz8sruMEY'
    b'SAMWYAlwHGw3RCgQJNIM8fO7n+TeT21hturT9CWvnNjJa5dfomtBhqQXJ+5FiHlhOqNpLCHI'
    b'HskeBopSXVQHSvXZ4Z5UDxgFUrQgEqQQSAme9OhLDFBrgPZtdp78Hb/PvkLn/AwJL0abF6Et'
    b'HCXuhelNLWRo6NRl/7h/ADAWkzSK8bly3+39X7taKtMUdQhIhC2xLQvXdjFCUy2UibtJ9o++'
    b'zpvTu0j3pGgLRYkEPaKhMOFAgEy4nbl6kT0/3fuMGlb7AN8C0MN6sLGiOrB08WcGrpSm0ZZC'
    b'2ha2tHAtm1A4yFj9LO9OHeA8QyQ7EsQCEcKBINFgmJjn0RlJEw5GefbZ7Qdzv8k/DuRoBQEo'
    b'VO6lKw+Nz4z8/fbFy4m4UbT2AQMIMIJgJISdtAnFwlhYCEGrgBLavRTxUIJfv/r84OhT534E'
    b'XLj+H1xTgUrpX4X9zfmVTy9ZtnRJwPaoNKsYoVtRWQ6u7eBYDo5j4doO0WCEnlg3hXqJJ59+'
    b'5vA/tw0+xhwfAOp6e26VheM+4D666Av9WxOZzh7lt15YYRkCrkPKayMdSZKKxrEsycl/n8we'
    b'fPHQjuq+6gvAuRvNPx5wTRl6nTudb2Tu6ron0Z28LerF0gEngCUFtXp1+sr57PDYobH3Gh80'
    b'/sxVTgKlj7P5ZMB1BXHpRBIHJAZQ1PDJAzO3Tnyr/gNyndAFrbDhdwAAAABJRU5ErkJggg==')
index.append('next_24')
catalog['next_24'] = next_24

#----------------------------------------------------------------------
open_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAWCAYAAADJqhx8AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAIhJREFUOI1j/P//PwMlgIki3aMGYBqgXrDDgVIX1KsX7Liv'
    b'XrAjgVwDGBgYGBQYGBjmQw0i6CJ8YaDAwMCwX71gx358BhETiA5Qg/KxSbIQYcADBgaGhJsT'
    b'PA4S44ILaPwJDAwMBrg0Y3PBBySDEm5O8LhIyHnYDCi4OcFjIiGNMMA4mp2HgwEAK5Unw3iO'
    b'ZHcAAAAASUVORK5CYII=')
index.append('open-hover-trans')
catalog['open-hover-trans'] = open_hover_trans

#----------------------------------------------------------------------
open_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAWCAYAAADJqhx8AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAIZJREFUOI3tk8sJgDAQRJ9iIZagHaSUdKCl2JHYgVagJdjB'
    b'eFGQNfGDN3FgDkmYx+xCEkm8Ufoq/QOCAPeYIGnvVtIoyZv7qEOATaMkdwU420EOtKvjo500'
    b'sKpCDbIba5oAD3ShRztCb84NUMTCwKHBvAN5YLiqZxvMQA2Ud8IAyf+dvwBYAAo3rlh8Dbv6'
    b'AAAAAElFTkSuQmCC')
index.append('open-normal-trans')
catalog['open-normal-trans'] = open_normal_trans

#----------------------------------------------------------------------
path_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAcCAYAAAATFf3WAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAASNJREFUWIXtljFKA0EUhr81apGk8ATqTGNrlSPIEEjhFUyr'
    b'YGdpZeMZLCyDIFjJnMIDWMxAiii2okViWIu1WATjG56aRebrdnlv5ts3w88WZVnSZFaWLfAd'
    b'WVBLFtSymlLsje189BQLyl5dDFOVVY1CGjPe2D3gAOgC6wtKL4ETYOBiGGsFRRP0xm4CR8DQ'
    b'xfAkqN8CToGhTk84QW/sMbAD3CD7qDZwDhx+en/nYnhIEZTeQQe0gH1gLuy5Bfq15y5wBuyK'
    b'7ZALPgMjF8N1yuJ1vLHbwFVqnzRm5sBb6uI/QeNzMAtq+TeCL8DsN0W+Qiq4RpWDf07jj1ga'
    b'1BOg543tKfbaoDqJJKSC91TTTt6gxiNwkdok/t1aFo2/g1lQSxbU8g6Glzctx5BiaQAAAABJ'
    b'RU5ErkJggg==')
index.append('path-click-trans')
catalog['path-click-trans'] = path_click_trans

#----------------------------------------------------------------------
path_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAcCAYAAAATFf3WAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAASFJREFUWIXtlqFOBDEQhr894MSxgicAHBZ1to4QEkRfgbOQ'
    b'4CpRiPIMiJOEhBSF7wvwAEgEECwBAWwWsYgNCXfTDLAb0s/tZqb9dtr82aKua/rMoGuBeWRB'
    b'LVlQy2JKsfVx+bOnmFH2Epx5VVm1KKQxY33cAvaAEhjOKJ0CDtgNztxqBUUTtD6uAgfAJDjz'
    b'KKhfA46AiU5POEHr4yGwAVwi+6gRcALsf3l/HZy5TxGU3sFtYAGwQCXsuQJ2Ws8lcAxsiu2Q'
    b'Cz4BZ8GZi5TF21gf14Hz1D5pzFTAe+riP0HvczALavk3gs/A22+KfIdUcIkmB/+c3h+xNKjv'
    b'gLH1cazYa4XmJJKQCt7QTDt5gxYPwGlqk/h3qyt6fwezoJYsqOUDfzA4bYXlJWgAAAAASUVO'
    b'RK5CYII=')
index.append('path-hover-trans')
catalog['path-hover-trans'] = path_hover_trans

#----------------------------------------------------------------------
path_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAcCAYAAAATFf3WAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAJBJREFUWIXt19EJgCAQgOHfaIfemqIZGqA9mqEp2qFpgtZo'
    b'CXsPotMrFbkffBP5IurQee8puSY34C0DajOgtqqAI+CF6wD6lMAemIEOcIK1AUtK4ATswCnc'
    b'vwJDlOiWE06SL8eNC9nc/nXwQ8EPWtVXnCUDajOgNgNqC/lRZ7m8SIFfTJGoin/FBtRmQG3F'
    b'Ay/nnRkH0sh4jgAAAABJRU5ErkJggg==')
index.append('path-normal-trans')
catalog['path-normal-trans'] = path_normal_trans

#----------------------------------------------------------------------
pencil_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAXFJREFUOI3N1L1rVEEUxuFnxT/AUiyEmcJGAtoF/MJGp1ME'
    b'P5o0hsRCwU4LXQIxTRSFtRUEC7E0YuEUNjZa2qR1BqyDWIhYCGuxd+WyXvUSIviW58z85j1n'
    b'zsxgPB7bSe3aUdq/AO7uCuYQF7GKfZhLtWz2Bf7iMId4BSu4i2MY5hAPbQuYQzyNEUaplhG+'
    b'4AIebdfhNaymWu7nEE+YlH0YL3KIr3OIe/8GHLTHJoeYsIAN3ML1VMubJncTB3A11fKtl8NU'
    b'S8ZLPMbSFNbk1k1acK+3w5bT2ziJi6mWrVZ8D55gEyuplu9/dNhys4a3WJ+Jf061nMERLHXt'
    b'/e1gp1qGGOQQ73SkF3E8h3gphzjoBWx0A3M5xIczh30wKf0ZTvUGplq2Ui1ncTCHeHkazyHO'
    b'YxnncbS9p/PpdWgZaznEr3iPByYz+qrJD6cLO2+5SznE/XiHTw3geauSn33s/dukWj7iHJ62'
    b'YbPq7bCv/v8P9gfqe3o7IZI6AQAAAABJRU5ErkJggg==')
index.append('pencil-click-trans')
catalog['pencil-click-trans'] = pencil_click_trans

#----------------------------------------------------------------------
pencil_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAXBJREFUOI3N1D1rVUEQxvHfFT+ApfgBbCSgxYLgGzZqpwi+'
    b'NBZrSIQ1YGcKvQRimigRrsU2gouF2AgqFrGwsbHZwiZtGusUKUQshGtxbuAQT/QQIzjlvDz7'
    b'n2VmBuPx2F7avj1V+xeC+7ucMddpLOIQpkoKa30FfyGMud7CAh7iFIYx16O7Eoy5nscIo5LC'
    b'CF9xFU93SziHxZLCSsz1jKbtY3gbc/0Qcz34J8FBe2xirhdwA29wD3dKCh8nsXkcxu2Swvde'
    b'hCWF93iHZ5jZEpvEljVf8Kg3YYv0Ps7iWklho+U/gOdYw0JJ4cdvCVs0S/iE5W3+zZLCRZzA'
    b'TFftjoNdUhhiEHN90BGexumY6/WY66CX4MTuYirm+mTbY+ua1l/iXG/BksJGSeESjsRcb275'
    b'Y67HMYsrONmu6Vy9DpvFUsz1Gz7jsWZGVyfxYS/CFuk65rGCV5q1XO3K7X1tSgpfcBkv8Hqn'
    b'vM45/Bv7/w/sT4ebdkuJ/xa5AAAAAElFTkSuQmCC')
index.append('pencil-hover-trans')
catalog['pencil-hover-trans'] = pencil_hover_trans

#----------------------------------------------------------------------
pencil_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAQdJREFUOI3l1C1LREEYxfGzYjAaNpgsBoMGi2gQjBotC2YF'
    b'xWQwKGITP4CatYnYfKkKJotF8BsINpvF9jPsVa7rheUui8UDD8ycZ/gzZ+CZBtJPDfSV9pfA'
    b'1SSvSSSZrEVEZ63jBZuYwwWmKs5VVqexgA9sFfspbT32CrzBbrGex3UB3cMtRuoCF3GGFp4K'
    b'6FdvGycYqgMMlvGO6YreIY7rAlNEvEOzwx/GFQ4wWAcY7BcRq3r32KgLDE4LcKc/hvPieRp1'
    b'gE1c4qiit6ithbLfbfTekiwlmUiyUvJnk6wlaSWZ6zYpVVWOOI6H0g3ViVyuUbziGUt+qidg'
    b'MIMdv/V9psF/+2A/AUoiASS9tiF/AAAAAElFTkSuQmCC')
index.append('pencil-normal-trans')
catalog['pencil-normal-trans'] = pencil_normal_trans

#----------------------------------------------------------------------
play_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAYAAACAl21KAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAANRJREFUOI3V00sKwjAUheH/FgUdO3MBDe7Cod2I02QpdtpN'
    b'OEy2Yue6haKg10Gt1kesoggeCJQSvl5OE1FVvpHkK8r/QsaFziJ77yLGhTGwnlZLKYqC5mdF'
    b'IeNCAuxv35d5tgEE63U+R+4mMi70gV3XhKn1WuaZlHkmWK9QY+2OBl3IaSJJa+AqbejwChRL'
    b'Enn+COrsBy4dRaHVYrYFhsCIuq/JI6hBUut1Wi3PoDy7tMaFAVCdPiQAInJG2ucIVX24mqgq'
    b'qfUa29espxO9kz+9/T+Fjl/1d79zyMbJAAAAAElFTkSuQmCC')
index.append('play-hover-trans')
catalog['play-hover-trans'] = play_hover_trans

#----------------------------------------------------------------------
play_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAYAAACAl21KAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAKlJREFUOI3tlFEKwjAQRGeCYr/99ASeLLm5hxDa8aPNuilJ'
    b'LFgEoQMLJZt9TCdNKQl7KOxC+WvQxyC3gAoIyRsApZRA0tZPrWmSQdJYaT1IUvNxG4n5+Eme'
    b'JT07zvKQuFjxMP9qQwfinWY3hTxo2gJqKTSevwL18jFJsozWDSvMOV0BXADcVQo+GkmKMb5n'
    b'PWhdAIYaKEO8Eapx+7P7pV98M9X9x2/kd6AXuPeEtJwbEd0AAAAASUVORK5CYII=')
index.append('play-normal-trans')
catalog['play-normal-trans'] = play_normal_trans

#----------------------------------------------------------------------
pointer_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAVVJREFUOI2t1DFrVTEYxvFfxaWDFDo5iYlKdXDyI3QwkyC4'
    b'C4Kbg25OUvoRLE4OhYrFqYtLhoKDlS6iTuKUQBHpUK6oaAWR63AOcjnWcs/hPlPyhvzzvG/e'
    b'ZG48HpulTsyUhpOTkxziAm5iM9VyMATYdbiIB9jNId4aApzr1jCHmHEVI1TcTbXsDHUIz/C1'
    b'dXsFT3OIj3OI54Y6PI1XiBPhQ+xhA49SLV+mdphq2ceLTngeS7iPdznEG1MDWz3X1LCrUziL'
    b'9b7Al/h0RPwH3uJSL2CqZYTtI5Z+4Umq5WNfhzRp77fjET5jAXdyiGkIcBff8RO3NXX7prn9'
    b'tRzihV7AVMshHmIl1bKFVey0B5zHVg7xTHffP314nHKI83iDi5re3E61XJvK4TGur+O1pjeX'
    b'c4hLg4Et9APuaZ7nmuYF/VWvlCeVQ7yM96mW3zMB/k8z/7H/ADscb4jM90ClAAAAAElFTkSu'
    b'QmCC')
index.append('pointer-click-trans')
catalog['pointer-click-trans'] = pointer_click_trans

#----------------------------------------------------------------------
pointer_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAWRJREFUOI2t1MGrzUEYxvHPlY0o4dpQStze1d24ZWHFbiJl'
    b'YWODLJRQc7NXspJOTZJkwU5KqZPNkI3c8h9gikiSIlsrHYv7W5yO3O7vOM9q3nea7/vM2zsz'
    b'NxqNzFIbZkrDxvEgct2KM3jYSvoxDXDS4XZcwjByPTcNcG6yh5HrI1Sc6gpeayWtTOtQB1vE'
    b'cdzGlch1ELnu+x/gAra0koY4j68YRK7LXZ/XD2wlfcN7HO7i762kAZaxHy8i15N9HMJLHJso'
    b'9LGVdBHPcKcv8BXmI9e948nIdYhDONAL2Er6ibdIHWhn5LobO/C0lfSlr0N4jqOR665ufROX'
    b'sRS5pmmArzGPFVzHJ1ywOkpXI9eFXsBW0i/cR2klPcENbMYR3MWDyHXP5Lm/Xspailw3WZ2A'
    b'W9iGpVbS2XU5XMP1aZzABxyMXGNqYAd9h4J7eIzP4/u9rjyuyHURb1pJv2cC/Jdm/mP/AXss'
    b'dosPEfREAAAAAElFTkSuQmCC')
index.append('pointer-hover-trans')
catalog['pointer-hover-trans'] = pointer_hover_trans

#----------------------------------------------------------------------
pointer_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAUtJREFUOI2tlL8rxHEYx19nu+ny40pMl2S6ASXpJtMtIill'
    b'kBSj0v0FSjYGYSCbzLhFmSQMikWUQuksBqtJL8N9r871PXffc+96hs/zfD7vz/O8n8/niak0'
    b'Ey1NZQshTABLQEfDjGq5pdQn9VKdr4jVZZUZvgK3wB4wDZwBmSgJhml4CqSBMWALyAHrQE8j'
    b'JaN2qidqW7BOqjn1SF1WE3+VXC2woU6G6Lut3qhTUQnH1f0qsVX1o96mlHBB8emkKvzHwAgw'
    b'EKUpAJ/AI5AN1kmgG2gH8kAhSlNKNqrm1S71Tj1U+9UDNRtVQ9S4eq2+BA1aU3fVYfVK7Q07'
    b'F6sxHBaAOLBJ8VvuAPfAO7AIzABv5QdqEVYiDpwHF7QCg8Bc+Yao0+YLmAUmgGdgCOj7taOR'
    b'AaBm1IK6Emhdt4Z/IQ08AN/lzv8QhqLpE/sHFJ/dsH79xXUAAAAASUVORK5CYII=')
index.append('pointer-normal-trans')
catalog['pointer-normal-trans'] = pointer_normal_trans

#----------------------------------------------------------------------
previous_24 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAABg1JREFUSImFlduPlVcdhp/1re+8j7OHzC4OMzCIQIaZDnI2'
    b'lGlJKYmxnq6atGovqqUBrxrlotFEU5M2NibUiybVC1MSEkIabFICldE2ytChOAiVAC1HKTDD'
    b'dM/MZp9P31rLi41TJpT4/gHv867faQl+zXwZkEKijJKO7TyxOLVke3ds0fq0n+42kDFGz87q'
    b'2Ymbp26M37j92Yg+ov9CgYgHSNwHiMBxne9s6R7evbHrG5vTTidaaZTWaK3QGIwAGcBMNMP4'
    b'lY9OjP35+Gv6r/rg/wco3J5k7++eXvnDny70upmuzFBulol0BBi0MSij0WgAfDsgk+xg2pvi'
    b'4DsH/ji5d+JF8pTvBUi2ziX3VmUH/7RjYNdzsuUyUZqkETXQ7cwoo4mERguDERqFpmbqzNby'
    b'xKI469ZtWJvrvd0/c3LmCE0aXwAeAxQsSve8/sLArudKlQr5eh6NQaPmEjdNRKFUpFqrYmyD'
    b'sAUKjbEMpahM1NCs7v/6yivupe7KP8uHMO1nSh4F13a/tWNw5x4ZueRreYwwKK1QRqGFpqaa'
    b'1Is1vj/wJI/0beLK7asURBlsUJZGS0PVVBGRZPma5UNnr5y5qq/rj9uAYZwtvY/uXZfZ1D1R'
    b'msRgiFAoE6GFoabr1O6UeWHLj/n2um+y7KGlWEZy7NYYTsJFW6ClBikoqQpd4UOohc3lt47e'
    b'3I+iZklXbtuU3bw+V51BG41CobSaM6/eqbBz+Hm2DgzPNW6yMkXdblLUZWajPPmowJ2oQJ0G'
    b'N4oTrOwf7Jfr5XcB7EXJnu0Zt5OJ6uRcM7XQc+a7tsw333tqPz8ffYlyvIVVsgCDLW0sYyGE'
    b'AGNYbT1MZmjBttzxqbfsJYm+9VEUEenobmM1TdOidqfKruHn2brqC/ND599j96GXML7FgkYK'
    b'aUmEEBRNCSshsYSgqZpMl6ZJ9qcGc/bUAjvtpb+idHtSjAAD5Kdn2fnIT+aZA2zu28T5n41j'
    b'WzbGgBCAgYPn3uUX4y8jUhaecrGlxAkSXVikLY3JKK0QwsJg+PDaGPVmk+1Dj9+3lR1Bmkws'
    b'QzJIkgqTJIMkyTDJs2ufYVl8Cb7jEPcDfNdDulYSQWgDs1LKVC2q8cGVY1zLX+S69R9Gzn/A'
    b'E/1b5wFmq3mEEEgkxrQHXSI4dm2MqqzQEUuhlCIVxCncqZXQRHaRwmS1Ve07cmGEydINCH1K'
    b'Vpmn9v+AA8/sY9uKx+YAhz89yq/+9hsSmTihF+JaNo6U1K0GyWwMy7JoRC1SYYKp+mc5NGUp'
    b'lorVFae18ez10+D74AgIbOp+hUPn3mN9dh19nYsBeHjhAI7l8uH0GH7WxU+5eGmHRDpO6AX4'
    b'drv+2VQXZ46cPlY6Udoni7Io00MLnp4tVFBW1Aa4FgQOdafG4fMjbOhay5LOXrSGDT1raFQj'
    b'LlYu0JnuIOHHiHsBgevh2g6pIInWitE3R/9gbpljlj6lRwr53L8Wd/W0j5IFSECA64UUYiWe'
    b'PbyD9y+OYlntUvUkevGkS9wPSAYh6TBBRyxBKhajr7OX86fPXVbj6mj7VLRQJYq5pcNffapc'
    b'atIwVfAllm0hLYvQC2n5LUavjuKpkMnC57xz/W1kBtKxBAk/RiIMCT2PbDxLrjLL2788+Jq+'
    b'rg8DSgLoG/qTarbYs2Jw1ZqZcoFINhGOjWNJHGkT8wKIaU7mPuJkfgzToehIpIh5AUk/JBnE'
    b'6E5kEbbN719541DhQOFVIM/dYoCG+qX6+2pFs3/Fiv6VlWadmq5iWxLHdnCkje94xBMxYskY'
    b'cT8kcFx8xyPwXHqS3UjbZc/rb/z94quXd6O53F7B/wEA6jTLH5cOV1PFhV9bs3x13ElRixoY'
    b'FFJaONLGkQ6utHFsG9d2yAQpFqW6uVmY4rcv73n301cu7abF2XbktsR96wrIrfJHi7+37MWu'
    b'vu4hY1moKMK2JaHrkwripGNJOhMpWq0GZ8bPfPKPN0ffMsfNPuDWveYPBADg0iE3yiczg53b'
    b'OwYWDMXCeJftyqRjZKlWq+Zy//78wsT4xKg+oUfulqT5ZTYPBtwrhyyCFBBiiNCUUUzD/A/+'
    b'y/Rf/aq8FazYU2YAAAAASUVORK5CYII=')
index.append('previous_24')
catalog['previous_24'] = previous_24

#----------------------------------------------------------------------
process_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAjdJREFUSInF1UvoTVEUx/HP9X7lMTA3u8nAI8lMyuP8ByaS'
    b'UhSp/51xywQRA0qSDrOTxEBJKQzkyiMGDEQUypYQBkomJPw9rsHZl+M6/79zQ1bt2metdfb3'
    b'rP3be51au932P2xE1cR6szUek/EqpMnAn4KHDQIZWZjX4nQP7uF4vdka96fg0opDmnyqN1vL'
    b'8C6kyeXoni+veDm2ItSbrSWohTQ53yu4VqZxvdlaiNMYEyFfsQudSg/iCfZjAKtDmpzsBTyY'
    b'xqMwQS7FvpL4hsJ8NBroCVyqcdy6zRXXeIYdvUAZ+lS/7Xp+Iq9qDNbJdwRCSJPrvYJ/0jhe'
    b'mR2Yh7kYH0OPsDykyd2YtwIn5Ds2gPu4gb0hTR5XAXdXPAWb/CrBqQ402iV8kB+2UZgdx3Ps'
    b'rgLuBrzGuZK80V3Pc+RbXrT3eFMFSsl1is1hOlbJqyfXez2uYwaOYWqMPccW3MaLkCaV4KX3'
    b'OH7AWhzpcr/BxC7fxZAmi6vAfguuN1sL5DoOr7DGezRxKKRJ5T/OUA3kSwS/lPfoBej08Gd4'
    b'gEUYK5flcHxHo9E4immF9WbiTpZlCzuOwRrIBazEeaxBH24WUraHNFmK1TiLbSFNvhTiR+KH'
    b'dsZk7CwySsERfgZ9IU0uhjT5jFuF8P2YcxzLQppcK76bZdlVea/v2JXo+25D/o+7NNsr3+KP'
    b'+N4kHh7oa9cO/EgqnJm1eKqkWoY41X/DGo3GRszKsmzdL8F2u/1PR39//6Qy/zfSUg4HG5tr'
    b'8QAAAABJRU5ErkJggg==')
index.append('process-hover-trans')
catalog['process-hover-trans'] = process_hover_trans

#----------------------------------------------------------------------
process_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAx1JREFUSInFVV9IU3EU/ja2clotfQrLMIki++eUMCOyzJSi'
    b'P1gWQUVFdAcrsP8RFYuIghVEGeFeZi89pkHq0AmtHlppREQP5cqpkTprrbvt3utu93p6yLvu'
    b'dAsdQh+ch3t+P37fOd/5LkdDRPgf0Kk/NBpN0osGgyEjKzNzdpBlv/EcJya7N+FGiCgWsWp0'
    b'Or26HoPBgIaGxtofgUCwubX9UVr6zPSJvPevSEgMAFarddux48fLAKCkpASyLHfSKJYWFi8G'
    b'gK07qirWllVUThlxTU3NBiJiiSjqcDhOezyek0TEKcRNzS13bt+9d0ImGuGE6PDWqurqKSG2'
    b'WCyVRCTTBFH38LFryqR2OOrPqh+XJJk4fngcae9Xf+8y0+o1kyXWjjWHXq+HyWRCfv6SsDrf'
    b'Mxj0dbz33gyHI7UAIkp+YKD/YyQ49CKZ2ZJCXYXRaMxwOp22YDDoJqKI0pX465c3zA8vD3M8'
    b'WJZFt89XrRpFdGBw8E1Ti7Nucf6yvJSkzs7OnsfzXNxsJUmmYChiU+6Iooi2trZMUplNwXnr'
    b'9YspSS0IQuDTZ59TndNqNaARefpPloUoiuA4Drm5uYUA0saIJyxakBNKSWoAmJM9L/3gEaao'
    b'1eW69bdrKdTl9e52u91zX3V0VkQ4fihmrn5/36kL1n1bdlTnL8hbOCslqdW4fuPGoXEW/vNv'
    b'x6G794trpjErYSOTJi5eu75UlCQpAXEi8DbbTUar1WomQ6xREypLYvW68k2eZ64mANPedfUN'
    b'CmzgffEqUykAPQD0+7/3Dfn9HwpWLC0HoP3246c7J2d+eZQPy0QEs9n8AECuSsCVAN7a7fYN'
    b'Me8kmvvL5+0uyzHLHrens3X7rr0Hdu6s2hwIBF4r53fu110u21hWeerMuf0fvL7mEyfPXYoK'
    b'nKx6oh5AqSpmA7jyT3OpodXpYnvySXNLraLt4aPmIiU/3TAjbpcqbzEM08gwDI3G07FSx+3j'
    b'sRiRpFg1165etbGhUJ8gDEfbW9u6lXxUiCRbwIcA9CTsFoif8VTDbDbXACiw2+2Hxx1O1IWp'
    b'BsMwxkT533IfNNyjqcHwAAAAAElFTkSuQmCC')
index.append('process-normal-trans')
catalog['process-normal-trans'] = process_normal_trans

#----------------------------------------------------------------------
random_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAedJREFUSInF1U1r1FAUxvFfpZa2qLOwrbrwBRGzUGmXuvJl'
    b'FTfFl7WiCxt3xg8g+AFEsh0QLH4ABRGMIlhE0IWgohSyKLpQqgjaqkhRMC4SYZrOlE6n1Qsh'
    b'Oefm4Z/n3Jtzu/I89z/GmuWIgjgdCOJ03T8H4w5urCg4iNODQZweaiUI4nQA2/CpE3B3k9xJ'
    b'bMBEC80JPEOtE3CzUg9i+98giNP+IE57yuceHMHd8uNWFPwba4M47Svjm3gVxGk39qIf97C1'
    b'E3CzUvfhGzbjDXoU63m8BD/AFw2lDuJ0P2RJ+HSp4HmOgzjtLcHT2FP+MrtxCacxgtuYMb/U'
    b'5zC0VOgCMDZhDq+xCwfwKEvChwrnM1kSvs2SMMfXIE5rQZzuU7i/3w64WuohzCLD0TI3Wd4v'
    b'orFpvFNswlN4kiXhXCfgwRI8ifPYiHHIknCy8u4sdmIYV9uBNgNvUWyk9wp36/GyhXYWIZ5n'
    b'STjdLri6xlN4nCXhT3xGb5aEH1pof2EU19qFUnGcJeFEQ/gdHxfR1hSup6oTURSNY0dDahgv'
    b'6vX64abgyriCH60msyQcXUR73cKWe7kx6Fqt8ziKols4VoYTjW5Z/rG4lHFG0WiouGUVHUMU'
    b'RRcwUq/Xzy6YzPN8Va+xsbFas/wfS7PVIdwUrGsAAAAASUVORK5CYII=')
index.append('random-hover-trans')
catalog['random-hover-trans'] = random_hover_trans

#----------------------------------------------------------------------
random_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAbdJREFUSInF1c1vTFEYx/FPhUYFs2mLiJdIY4O0O6y8rNg0'
    b'WmvCwtyl+AMk/gD/wF2xsiSxESIxsdEgQUgTi4YFRZrQQURI3C7OWdy5c2fM3NF4kpNznnPu'
    b'c7/P78l5GcqyzP+wNRXjRrFxEPBQRcVzWMRsVXCZ4iM42iVmFDuxVBUKa0vmTmMzGh1iZvEU'
    b'tUHAZYrHsCvnb8BwHA/jOO7E5P4p+A/WYST6N/FSqM7+mMhd7BgEXFbqEXzDVrwRVC5hJoLv'
    b'44vWUh+K/Vyv4KLi9RH8AfuEI7MXl3EWU7iNZa2lvoDxXqFl4C34iVeYwGE8xANB+TLeIsNX'
    b'QfWB2N/rB1ws9TiaeI2TcW4+9pe0XhrvhE14Bo9iwj1bUfFYBM/Hnx7Ek1wCj3PfNrEHk7jR'
    b'D5R2xduEjfReULcJLzrENnECz4Q9MRB4IbZf+Izt+Ngh9jemhZuubyuCG7nxd3zqElsTVC8U'
    b'F5IkuY7dualJPE/T9FgncN6u4keX9ekua9e0X7lX8k7V1+mvliTJLZyKbiOvlurvcS92Tjj3'
    b'FNSyioohSZKLmErT9HzbYpZlq9rq9XqtbH4F8SCzQi/Ay+QAAAAASUVORK5CYII=')
index.append('random-normal-trans')
catalog['random-normal-trans'] = random_normal_trans

#----------------------------------------------------------------------
recycle_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAWCAYAAADJqhx8AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAASFJREFUOI3d078rR1EYx/HXV8qvBUWkROSazQYZdFf5sTCZ'
    b'JMPd/A3KcCeL2aTYuAaLXwslmS4mKWWwG/haTrrdXCmD8mznnM/zPs/nPM+p1et1v4mGX2X/'
    b'D0BjeSNKsi7sYhz7WM/T+LgKUCt2IUqyPlygt6Tbwyq68jS+/rKCKMkagrAXZ3hEM6YwjQm8'
    b'YLjKwjIesJCn8V3Bzg1a0IHLsoUi4DRP483S+Sye0Y4mnJcBtZ9MYpRkg8HCSZ7G95WAKMk2'
    b'QqlH4banPI1fv4N/zkGUZK1YwBK2A2S0VMlkGVB8gwH0FNYHuI2SrB1DWMQM+qsAY7hCG0aw'
    b'grmg6Qya+UoLOMzTeCyAtvCO7pD8hrU8jXfKgB914bv4+9/4DwAf5ZJNUZG5OFUAAAAASUVO'
    b'RK5CYII=')
index.append('recycle-hover-trans')
catalog['recycle-hover-trans'] = recycle_hover_trans

#----------------------------------------------------------------------
recycle_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAWCAYAAADJqhx8AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAPpJREFUOI3dkzFKg0EQRl9SJdpo8TexErSxsRBbkRQ5Qexy'
    b'Ag/gKQQbK88gdjaCVRJJlV6ijYgxgloLwWfhXwxr3MI06gfLssvOm5lvdysq86g6V/T/BRRA'
    b'FxA4B3ayBDWOFfXBrzpTG+pmcp5KuMYqMAC2gT5wD9SAFlAHXoEXYO27CvbVU3U97BXqY6jk'
    b'Iq0getAD2sAo7LWBJ+CtXF+lFsQWcloFdvk09yYHOASWgcsy2zhkn63Qz4I6Dv3eznC9mXoQ'
    b'FxvJ1R2rdXVJ3VKP1LscoKMO1esS8K5O1OcA3csBinJeVE/UaQicqgdpcPqQfqTf+Rv/GOAD'
    b'lERinsbskcoAAAAASUVORK5CYII=')
index.append('recycle-normal-trans')
catalog['recycle-normal-trans'] = recycle_normal_trans

#----------------------------------------------------------------------
reset_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAS5JREFUOI3N1CtLBFEUwPHf+kIUQQyC0TRdu0EMo8IuGFTE'
    b'R7KYBoNfQTFNMfkIIohFEBHmG+gHEGGCiGIQLEaxjMFZcHVnd4UNnnQf5/75n3Mvt5RlmXZE'
    b'R1so7QR1FW0EUTKIOaxhDBnucIKzNA5fv+eX6vUoiJJRHKIPR7jAB6axmQssp3F4WwjKTc5x'
    b'n8bheoHtLqZQTuPwmfo9mkNvEQTSONzKh/PVtRpQECUV7OCtCPIt9lCuC8I+hvDSAugSQXXS'
    b'lZtkOMAtJtAfRMkxVtI4LBWAetFZY5Qnj6IHTxjHcAMIVPBQA8pjBtd4xw0Wm5S2kZeHH9cf'
    b'REk3PpqYCKJkG0uYTOPw/heoyeERzCLCABbSOLypa9QAsurrWTziCqdVkz+BWon/9418AsPf'
    b'YZ6+4IYfAAAAAElFTkSuQmCC')
index.append('reset-hover-trans')
catalog['reset-hover-trans'] = reset_hover_trans

#----------------------------------------------------------------------
reset_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAARBJREFUOI3NlD0vREEUhp9dkUg0q0CIRrR6foJotCKiWKIQ'
    b'GrVe4i9sovAXJCoRknvtFrJRbKnRkGxJoxCPZq5c3LluYiNO8hZnPp6ZOefN1FQGEfWBUP4K'
    b'1ACawBXwDDwBHWAXGP+2Wi3SrHqhdtRtdVIdU9fUG/VWnc/vKYI0AqQVOQT1SO2qM2Wgpnpd'
    b'AsnUVfdjoBW1r55VAG2qlzFQX31VjyuAJtTHLK8DpGkq0AJ6oQejwEkYj8UIMJQltZyzz8Pk'
    b'NPAG3AFLJaA9YB1YgM8+WgbawEvwy2oJBGAHOP3Ivrx7OEkSK9TnUL1X58raH9OUuqX2AmTx'
    b'J0MWaUN9UNvqQf4mmfLF/lX8v2/kHRYA4/PCNOsgAAAAAElFTkSuQmCC')
index.append('reset-normal-trans')
catalog['reset-normal-trans'] = reset_normal_trans

#----------------------------------------------------------------------
save_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAOJJREFUOI3Nk0sKwjAQhr+K+FiJG7eCiFlVr9Hb2KP0NvYa'
    b'vhYF9+4EQSiKOi5MZIiNXejCH4b+mQlf0hkSiQi/UOMnlL8ENfXCpPnS2hgQG1vAAG2AIkui'
    b'SpKIvGIyXyyVF68mVXkX/q8N9Rle7eZuZNL8bdRNb91Sfm3S/AD0LXStaqs6UNeZIktm/mal'
    b'cR3o4oxt/FTVTkBZZMlAHxgC7ZXv+RNSU935IL/Zx4B3iu23rANpTStyUaj2CXStyJ1DmyP9'
    b'+k2a34ANMOLZvxZwt1ECPZ6jN0WWdIKgb/R/r/8BedRr5zE/61EAAAAASUVORK5CYII=')
index.append('save-hover-trans')
catalog['save-hover-trans'] = save_hover_trans

#----------------------------------------------------------------------
save_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAMBJREFUOI3Vk8sKwkAMRc+IKCLiJ/gDPv7/M6q4cy+4EKWI'
    b'r7bjwhRDmrYgXeiFkExu5xCmMyHGSBfqdUL5C1AiUQA5kMn6BkQJV32nt5IcgaD65dr23Ylm'
    b'ZqNWLjk4XgU0UPUGOMqmAtgqb21Bwdwjd2xHF2DcNNFD1QmfA45AChzEG1myBe1VPZXpypgo'
    b'f9cGOtfUpRaSr20graXTC3VeEyhzeve6jy1ozvuQUwHlwFMAJ2AofgVof//X+r3X/wKamjad'
    b'ZgBOvwAAAABJRU5ErkJggg==')
index.append('save-normal-trans')
catalog['save-normal-trans'] = save_normal_trans

#----------------------------------------------------------------------
show_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAPJJREFUOI3d07FOAkEQxvEfxJewxniJJTX0W1gTeQGoSI6C'
    b'p7BgEyt4AYy1xfVYU5KsgdrHwGaL8zgbpTBOM5Pv2/lnsrPbOZ1OLhHdi1D+N+jqO6Moq9Yt'
    b'pBg6bXqnubWirLbo4RpDHLPVwxYfOKYYhvW+bgPyiAFesEgxvGGEUa4X2Rvks+cTFWU1wQrr'
    b'FMO0ocE0xbDO+gqTulaf6CnnWYvWrGdNrQ66y3nfojXrfVP7ctlFWT1ggx3eUwzjoqz6kGLY'
    b'FWW1wS36GKcYnltBGbbEDe4xxyFbN1jiFYcUw7zedwaqAX/3jn4af++vXQz0CY6rXIXiqefL'
    b'AAAAAElFTkSuQmCC')
index.append('show-hover-trans')
catalog['show-hover-trans'] = show_hover_trans

#----------------------------------------------------------------------
show_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAM1JREFUOI3dk7ENwkAMRV8QSnagpqKkoQpzZAJaGrZIkzYT'
    b'wABMABVF2lTU7ACNKfhE1nGJhJQCYcmK9fztO/mcxMwYwyajdPnvRtOBXN8rJDEYu9EZuCnO'
    b'gZk8F7tJExxr5r20l1VmthPbyhGrpCl9rW+ykaCOMFP85nXIEreQdyAFMuARMMQyxalyHfMz'
    b'WujbRlgYtx8smFGhKzdmthdbyhFrpCl8bfj8B2AFzIECuABX5dZiR+AkbWd+RqF9tUdDCxkt'
    b'6LPf+9dGa/QE+lnROoR24cQAAAAASUVORK5CYII=')
index.append('show-normal-trans')
catalog['show-normal-trans'] = show_normal_trans

#----------------------------------------------------------------------
time_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAYAAACAl21KAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAU1JREFUOI3N1LFuE0EQxvGfI2RRpTJFXIR0l45Q8A5bIb8C'
    b'Sh3psITSxRKRLFGYHA2uEI+A6e4t4pRXxRIgF2mIQkFEYYps0HG+s4XkgmlW2pn573wzu9ta'
    b'LBY2YVsboWwS9GCVM0nzA+zhE54WWZg2xbbqepSkeQ8jdDBHghtcoV9k4XM1Z0lakuYDvMcb'
    b'dIos7EfXDoYYx5jmimIlY4QiCxcNchf4jhdFFiZNFY0wWAUpstCKlb2tlRYb+wgf10DgHbox'
    b'B39P7TF+FFn4VSNFCQK3cT1Hqyptgp37xHurAMp7X9FbkoYD/ES7LrF8QJLm2+7aMFsCxQbP'
    b'cVgF1cCO8K08lOrUXmKYpPmzNbBXMfaPLd3sJM1PkOIUH3AdAW0co4+zIguvV4Ii7DnO0MVD'
    b'XGIXX5DWPZFaUAn4BFN305k1XdS1oH+x/+9j+w1LuImmmtb2nQAAAABJRU5ErkJggg==')
index.append('time-hover-trans')
catalog['time-hover-trans'] = time_hover_trans

#----------------------------------------------------------------------
time_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAYAAACAl21KAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAQRJREFUOI3dlL1KxFAQRk/ETSNsZ+0jbBpfYzfvIIithZW4'
    b'+4i2NhsFQTv/EFxROBY7K5eQmygsFg4MN0wyZz5mJrdQ2YbtbIXyl6AKqAHjOW9ql9fqUn1W'
    b'r1zbS8RmXTldkIV6px6ro4ip7qlH8W4xBKrVe3WSUbqBPsa3WdAylPRBUM/UJgeqog+jAQhq'
    b'qa4iB5XdpO8HwCvw0Z5HnEUSe4/z8jveqmircpeajd+mE0z3qAJWQNmxJUWiDGAM7AM3uT1q'
    b'1JMfNPs8BpOd2kx9UA8HYE/qtA+EOg/YqTpOVJTqhesdmrfzclWnIf0tQI36qV77i18k9UmA'
    b'ZvZvO4X/9mL7Am+xjftg54OyAAAAAElFTkSuQmCC')
index.append('time-normal-trans')
catalog['time-normal-trans'] = time_normal_trans

#----------------------------------------------------------------------
up_24 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAA+JJREFUSImllcuLXEUUh79zTt3bPa+O6czkMZOYSBIxZiFm'
    b'IhpBcNvqXsmYlwkI5n/Qjf4Jioq2SxFEBMG1iyjB4EaJmokz3e1CHARJz0w/594qF/f2zCQ9'
    b'j4AFRd0q6v6+8zun6l7hA3ZvAczswnMz59679dWP7/Y/63/8EG8BYLy8yw4PojL32rHXP312'
    b'9IXy6ONjLy0md5f8bf/T/wd4iF08d/6xC9UpmYl/bd5hqnhAD549VKn1Hg6yPcBDwRXmLhy/'
    b'Uh0Pk/Fiqw6RsJKsUHZTemh2ulLv/7ErZGtALj53/HK1mJbixXYdHKR4fPCs9Fcpu0mdnp2p'
    b'1PsLO0KGAZvEC34irrUbiAmpT0mDJ+AJQKu/yt5on86cnanUe9tD7gd4KLri3KUTV6uRH49r'
    b'rQaokIYEj8eHFI8niCcItNZWKUeTenj2SKXeXljyvw1DNgAD8ZPXqlE6Fi+2G2CQhiwtHo8X'
    b'D5JtFwFVoZ12mCzs10dnj1RqKwtL/vf7IRkgF7988lo1TsfjWruBmRKAgCcJCWt+ja7v0k27'
    b'9HyPnu/R9z08Kc1ek73FfXrk6cOVRrO25Oc3IML7MGqjcxdPXK0W0om41mmQSMpq0qLZa7K8'
    b'tkw7aZOEBBRMFRPDTHGqiCiigopwYHw/lqTpzQ9vXO9/2/8IwNyr7vrF01c+OTpx3Jb4hzDi'
    b'ude/x+K/dRaW67SSNh6PmuLUcOaInCMyh5qxf2SS6dJByhN7iGLHdHlGy0+VX2ncq7XD3XDT'
    b'pV+mB76IPq8mPgkqEhKfdvecLj3/xLlnzvz1598UoxinbpO4rT+Lwr7xR7j19Y2fW3faPxBw'
    b'IXgQLHTCMZQpF74Jby/TvK/yRSm8oy/KGVPF1DAzTI3IGZE5nGWjqKCxsPLL6ved79pvbXFK'
    b'Yze0dBqkImhXcGKYKk6UyAaRZ+KROcw0G51GW90BoO8eFOdNwCHidT1ysywlLheOzBG5iMiU'
    b'2CLw28gDG4AngWtAALqgIuggRZo5ifLo47zIUZTNCdsDFIBTwBsb4qQgKvmRzI7jADQocOwc'
    b'sYsywI4OTgEXyTb189UUFEFF110407wbkW5KldmODhzn88h7+UoAEhARRAQbpEos63mhB/fB'
    b'yW4O0kxwvYXBXDDNxLN65CnLuzPL7ocZsiNg7YGVkKVIHtyZOxLJPgsqG8Cdmhuy50G86NjI'
    b'GKV+ifF4lKKLKUQxxThmJC5QjGKKUYGRYoHSSAlEtqU4VoYdrPZWO/Xb8+1C6sVLh570SDA6'
    b'oixvOlXOHPNunm632yczPVRuobAFNjDBGkeBAuS/sO2bYqyQUoOhhPMf3TF+Z01qI8AAAAAA'
    b'SUVORK5CYII=')
index.append('up_24')
catalog['up_24'] = up_24

#----------------------------------------------------------------------
vu_metre2 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAANoAAAAFCAIAAACsF2V2AAAAA3NCSVQICAjb4U/gAAABAklE'
    b'QVRIiWNgGAWjYNAARgYGBtdt7ljl/nz9czjhoONqZ6yyn+99vtp32WKKFVbZ95ff3V1616TD'
    b'FKvssz1P3196r12kg1X20YaH3199V0/TwCp7c9YNTjFOuQB5rLJX+64I6glKuUhjlT1TcVo5'
    b'WllQVwir7ImcY9pFurxKvFhl94futV1gz8LNglV2t9dOPMF4IueYzXw7rLIUBqPUmTfFaZpY'
    b'ZTfsePLyzff0GFWssjOX3BYX4QzwkMEq2zvruuErfncJCayyRRcuxivI6wsIYJVNO3O2XENd'
    b'mYcHq6z/kaOP//zBqpORgYEJq55RMAoGBIwmx1EwiMBochwFgwgAAH0VYAhA4kYpAAAAAElF'
    b'TkSuQmCC')
index.append('vu-metre2')
catalog['vu-metre2'] = vu_metre2

#----------------------------------------------------------------------
vu_metre_dark2 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAANoAAAAFCAIAAACsF2V2AAAAA3NCSVQICAjb4U/gAAAACXBI'
    b'WXMAAArwAAAK8AFCrDSYAAAA+ElEQVRIiWNgGAWjYNAARgYGBgsvDqxyf38znD/w08SVHavs'
    b't0//7176rWvDhlX207t/T27/0TLHLvv6yd9P7/4p67FilX3x4O/Pb//ltViwyj689oedi1FC'
    b'gRmr7N1Lv/mEmERlsMteO/lLRpWFT4gJq+zlI7+U9Vi5+Bixyp7Z/dPQgZ0Zu5MZTmz7gScY'
    b'Lx35aehIk2D8+eq/viZ22ftP/nz//k9LFbvstdu/ODmZFGWwB/LF67+k3zMrsmCX3ffjhw4r'
    b'qxgz9kDe+f27OTu7ABP2QF737VurlAwnNtmcxw+x6xkFo2BAwGhyHAWDCIwmx1EwiAAAHAVf'
    b'CAHlJsIAAAAASUVORK5CYII=')
index.append('vu-metre-dark2')
catalog['vu-metre-dark2'] = vu_metre_dark2

#----------------------------------------------------------------------
waves_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAZxJREFUSInNlT1IHEEYhp87EpNIOKuAmCIphCljJ2hh0sgU'
    b'SSGmCghR4abMVBb+gGJhIZKpggMqKXIoVukyKYQTSZFGbMfmGgsLC5sDC5O1cE6WdfVEbnJ5'
    b'YWH3fXfm+fh2dqaQJAntULEt1P8GLLQrCe0m/gX4Qea5CxgGNkIhA8AYcOKNnGslONvqIvAk'
    b'QPuBbeAX0CO0WxPaPY4FJkB7gWlg1Bv5zRs5CTwD3kYFA1PAT2/k75S3ALwX2nXHAncDj4BK'
    b'2vRG7gNHwIdWgAvpDURo9wKoAXXgzw2FdoY8b+cpAiPeyJ1m4OyqBvgBvPNG/s0bILRbBmre'
    b'yC852RrwvBm0UWFW5zdBg1aApewKF9oNAR1c/gn3At8qb+Qx8BlYFdo9DNCnwCKw7o08iwIO'
    b'8HmgBMwI7QaBLWDPG7l71zmy37gOHN5xrAJmAQ1UvJGbV4FSX4GXqXdfAQfW2jcNoxDjWFRK'
    b'DQHVjP3aWnvVkSinUwB8T1nVNDQaOOgjcBru57NhlFY3pJT6BPRZa8evhUmSRL3K5XJXnn8B'
    b'rJjPsTlXkigAAAAASUVORK5CYII=')
index.append('waves-hover-trans')
catalog['waves-hover-trans'] = waves_hover_trans

#----------------------------------------------------------------------
waves_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAWJJREFUSInN1TFIHEEYxfGfR2JUQqwE0UIL+6QLmEJsUiVF'
    b'iJVVYuC21CYWanFiYSFiZzJgSIpIxMpOLAJKsLAJ1jZpLAQtbAQLdVPcGpZ1zzvE5fJgYea9'
    b'mf0P7H7ftMRxrBkqNYX6P4GfYKwZ4E68TM0H8QlzRYNLaE/Gz7GOXfRgBW1Fga81gCm8xXd8'
    b'QBdeFQ2exBb2Ut4sRtBdFLgbj7Ca8X/jEKP3AW7JNJA+/MEZLnPWl9CR5Hmdp4Q3+FkP/CDH'
    b'28RrXNXYs5AcbjknW0FvPej1CbO6uAUKi5h38w8fQqtqJdwJXE9HWMJnPEy8x6q1/gXnRYGh'
    b'otrlpvECa/iFnUZfkP3GZzhocG+EGUyoVsCPf0EUfUN/au1T7IcQhmuBT/CxQfAxxmtkX7Gd'
    b'8SrpSSG3UwhhBxspazvxigUneofTZFzJhtkGcq+Komgcz0II72+EcRwX+pTL5c48/y9jqZ5n'
    b'LqtqxQAAAABJRU5ErkJggg==')
index.append('waves-normal-trans')
catalog['waves-normal-trans'] = waves_normal_trans

#----------------------------------------------------------------------
xfade_linear = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAPRJREFUKJF10kFOW0EQhOF5EXcKUiAbFIgwthITg/DRvMky'
    b'V2ABCAmMiHKNiGPUl808NB6/9GZ61P1PVbemYIOTUgPv55gnGcslyWf8LDhLcofvPdznSWa4'
    b'w2IsLvCEby3QPTDHFqvSBi7w3Co3tRn+4HrSSoW3WDb2zvGKddM3TMHzOscxPuGhVUqyC3Xw'
    b'If4mecNRr4TyoZ+nxkEpxTAMKaUM/+nZW/kS91X1Y81/7PV2Fpd1OfNuYS+42ltOvVxW6GLC'
    b'0SzJb9zsFJJc4hFfW0vtVxvhJOsRmuM2yenUzBNf7hGrgk2SL31jknfF7qFz/PoHNNxNwh8F'
    b'QxsAAAAASUVORK5CYII=')
index.append('xfade-linear')
catalog['xfade-linear'] = xfade_linear

#----------------------------------------------------------------------
xfade_power = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAUpJREFUKJFtkrFKnUEQhc+st7ERBIV4xYiND3BRCxEb7RS0'
    b'CiqCPoIggVT2liE3gZTqxVIE0auFFmlinSaVj5B0otX5bHYvvz//NLNn58zMmZ0N298jogP8'
    b'i4jfwEVK6a8k2VZKScCkpE/AqqSxiHiUJAEJmAO6wAOwp2zABtAHesAy0JKkUM2AFUkHwK+I'
    b'eJG0JuksIs7fEW3XcwV8tP0K/AemG+JKKaUBqAQWIuKPpCdJo9UESYqI91WygiXg3vY8sAPc'
    b'AuON6oDIftj2FXBYiX0DftS5si3bJfELcAqkCnHC9rXt3YwHs7WyXwRugE65LyRgM8ufzXio'
    b'dA3bJ8BRUQEMlGTyV9vd+oz7ti9tj5RCDfN/APq2t0q3Gdt3wHp9LcXKawLbtvu22wEcS0oR'
    b'8bm6mrKr8l+rkoFn2f4JtGvSG88ZT9nuvQEC6UR8F3lSlgAAAABJRU5ErkJggg==')
index.append('xfade-power')
catalog['xfade-power'] = xfade_power

#----------------------------------------------------------------------
xfade_sigmoid = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAATdJREFUKJF1kj1LlmEYho/rDmloUXBpEISGCNwskNbo8wdE'
    b'BjooCP2Clug3RENNUbRHS0tTGGri4uRgv6ChKWhoOY+Gnlef9zbv7brOj+s84S71tXoNOKyq'
    b'91V1CKCWWq21DPMKsAksAUcMywX1ufpVfUj3kmyou+pTda7HUe8n2UvyYCR6PIhunRF07uvq'
    b'J3VGXUyyk+R2x6HGQ2ttcvktsANcAVJVz4Y9VXXqoJ6JrG6rB+p8hwHQgGmXf+AecBn4XlU/'
    b'x4IJt/XZB/AX8Af4cV6qNnX+tOMCcBG4PiH2qU6ido6r6i7wW71zDmf6qTeTbKtXk9xVP6uz'
    b'/6s0Ft1L8k3dGu1eqe/USz35gnojycvhy611+Jz6Rv2QZPmks/oCWAT2gY9VdTwIJv2jzgBP'
    b'1EdVVeqXv48HAD7In3ZkAAAAAElFTkSuQmCC')
index.append('xfade-sigmoid')
catalog['xfade-sigmoid'] = xfade_sigmoid

#----------------------------------------------------------------------
zoom_click_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAbBJREFUOI2t1M+LTXEYx/HXHQwR0fiRMuqcZMFi1haEmpyy'
    b'HBYaFBt2ZHYWVlZqVjazIdxsNMnyy4b8KJv5C/A9kRoUShYucS3Ol7md7j1TzKdOT98f532e'
    b'5+lznla327WUGlpSGpb32wxZvgsXcADr04fn0cZMUcbPg4Ct3pJDlg/jLC5iU9r+c6GV4iuc'
    b'Lsr4tB+wXvIkphPsLa5gIj038R070A5ZPtaYYcjyUTzBdsxhoijjm97LIcsP4Rq2IhRlPNyU'
    b'4TFswzscqcOgKON9TKnacDAlMRC4L8W5ooyv+5WTdA+fsAL7m4C707rTAFOUsYMPabmzCfgt'
    b'xZEmYNKGFOebgHdSHAtZvnYQKWT5ODaq+vioCdjGD5WRryZP1mGjmMUwnuHFQGBRxpe4hJ84'
    b'gQchy/ck0EjI8vN4iHXplS0WzP9XrfpwCFl+S2WhoVRWByst/ClfsSadP8bJXov1Gw5ncFRl'
    b'7l8JBh9xF+M4hy/Yi9mQ5asHZljLdhU2o1OU8X3tbBI3sAzPcbwoY2wELqaQ5VO4nKCnijLe'
    b'/q95WJRxWtWi64gsUvK/aMkn9m+VAIbEZ1QSYQAAAABJRU5ErkJggg==')
index.append('zoom-click-trans')
catalog['zoom-click-trans'] = zoom_click_trans

#----------------------------------------------------------------------
zoom_hover_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAAWdJREFUOI211DFolDEUAODvtCgOpZU6CZ0zFtSlQ8VFyHaL'
    b'g6IUnboGXJwUB8FFSBHHFhcFwcFu0UVwcimcblkK7ejUSeniOdw/nOf959meb8wjH3nJy+v0'
    b'+32zjFMz1f4HONeWCKl0cRcL6OMAmzXH3iSwM3qHIZVFbOMyXuNzk+riFp7WHB//ywkfYhlr'
    b'NceDofWdkMobbIVUejXHnXHgb3cYUlnBTdwYwUDN8T3uY6vthKOP0sVuzXG/bQPe4WdI5eo0'
    b'YAdHEzA1xyN8w+I0ICxNAps4j8NpwB5WQirzbVJI5Tou4MtfweblengeUjkzBlvGW3zV0sPj'
    b'Sr6HNXwIqaw20FJIJeFjA11q8hdHN//R2A2wgEdYxzmcxT428QMvGvgT1odbbCw4KUIqc9jA'
    b'E8xjF9dqjt+PBQ7Bt/ESpw2+552a496xp03N8RUeGPTtFaxywvFVc3xmUP429jhByW0x8wH7'
    b'C158c2POAaS8AAAAAElFTkSuQmCC')
index.append('zoom-hover-trans')
catalog['zoom-hover-trans'] = zoom_hover_trans

#----------------------------------------------------------------------
zoom_normal_trans = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAK8AAACvABQqw0mAAAATNJREFUOI3NlL1KQ0EQRs+VYCFIlFgJRvAFUmthJ5a3tEhj'
    b'YyWI4AP4BArmCXwC8QnESkEJxM5CBUUsNEUsRPzLscjaxJvNhURwYJr92DOz3w6TqAwzRoZK'
    b'+wtgIaKlwCpQBATugD2gEQNmdTgBHAA14DJAagF6CmxHW1S7c1c9V8sZ2rJ6r6YZGuovYEV9'
    b'UGd7XVBX1GYvvfvJKVAHbiOPOgTawGIeDxPgLepRR3+k43VfIECpDxBgEmjlATaACjAegS0B'
    b'U8BFppph7JG6r45maDPqc5iCUp5fJvzwtXqszoezkrqpXqkv6pdaV6fzAFGLYR6bAfAZimyo'
    b'a+q72g5Fy3mAsSyo62ordHqmjg0C/Mmq+hE6PVHnBgWibqmvwYKqGt02eWIHeAIWgBuAxP++'
    b'sb8B+DgaoxP3ukQAAAAASUVORK5CYII=')
index.append('zoom-normal-trans')
catalog['zoom-normal-trans'] = zoom_normal_trans

