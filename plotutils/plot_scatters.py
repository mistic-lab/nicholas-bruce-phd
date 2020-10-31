import numpy as np
import plotly.graph_objects as go


# path = '/Users/nsbruce/Documents/UViip/size-10-res-0.05/normalized-amplitude/normalized-amplitude/'
# path = '/Users/nsbruce/Documents/UViip/size-10-res-0.05/'
# path = '/Users/nsbruce/Documents/UViip/size-3-res-0.01/'
# path='/Users/nsbruce/Documents/UViip/size-10-res-0.05/gridded-model/'
# path='/Users/nsbruce/Documents/UViip/size-10-res-0.05/model-only/'
path='/Users/nsbruce/Documents/UViip/vis-modelling-results/sim-vis-img/'

def point_source_visibility_model(u, v, l, m):
    '''
    Computes visibility at u,v as if from a perfect point source located at (l,m)
    '''
    return np.exp(2j * np.pi * (l*u + v*m))

def get_nscatters(*args, **kwargs):
    """
    Takes as many data series as you want as dicts with keys: 'x','y','z','name','color'

    Also can take kwargs for 'xlabel', 'ylabel', 'zlabel'

    Returns a plotly figure (typical use will be to fig.show() or fig.write_html('name.html'))

    i.e. fig= get_nscatters( 
        {x:np.arange(10), y:np.arange(10), z:np.arange(10), name:'Blah', color:'red'},
        {x:np.array(), y:np.array(), z:np.array(), name:'Blah2', color:'black'})
    """
    data = []

    if 'xlabel' not in kwargs.keys():
        xlabel='x'
    if 'ylabel' not in kwargs.keys():
        ylabel='y'
    if 'zlabel' not in kwargs.keys():
        zlabel='z'

    for arg in args:
        data.append(go.Scatter3d(x=arg['x'], y=arg['y'], z=arg['z'], mode='markers', marker=dict(size=1,color=arg['color']),name=arg['name']))

    fig = go.Figure(data=data)
    fig.update_layout(scene=dict(
        xaxis_title=kwargs['xlabel'],
        yaxis_title=kwargs['ylabel'],
        zaxis_title=kwargs['zlabel']))

    return fig

# ## General from a single image-model-fittin.py run
# ug = np.load(path+'gridded-u0.npy')
# vg = np.load(path+'gridded-v0.npy')
# visg=np.load(path+'gridded-vis0.npy')

# uvwr = np.load(path+'uvw0.npy')
# visr = np.load(path+'vis0.npy')


# ug = ug.flatten()
# vg = vg.flatten()
# visg = visg.flatten()
# visr=visr[:,0]
# ur=uvwr[:,0,0]
# vr=uvwr[:,1,0]

# dr={'x':ur, 'y':vr, 'z':np.angle(visr), 'name':'Raw', 'color':'red'}
# # dr={'x':ur, 'y':vr, 'z':np.zeros(visr.shape), 'name':'Raw', 'color':'red'}

# #! NOTE THE NEGATIVE
# dg={'x':-vg, 'y':ug, 'z':-np.angle(visg), 'name':'Gridded', 'color':'black'} # works
# # dg={'x':-vg, 'y':ug, 'z':np.abs(visg), 'name':'Gridded', 'color':'black'} # mag
# # dg={'x':-ug, 'y':vg, 'z':np.zeros(visr.shape), 'name':'Gridded', 'color':'black'} #zeroed

# fig=get_nscatters(dr, dg, xlabel='u', ylabel='v', zlabel='vis phase')

## Models
#raw
# visr_model = point_source_visibility_model(ur, vr, 0.22, 0.32)
# drm={'x':ur, 'y':vr, 'z':np.angle(visr_model), 'name':'Raw model', 'color':'blue'}
# #gridded
# visg_model = point_source_visibility_model(ug, vg, 0.22, 0.32)
# dgm={'x':ug, 'y':vg, 'z':np.angle(visg_model), 'name':'Gridded model', 'color':'green'}

# fig=get_nscatters(dr,dg,drm,dgm,xlabel='u',ylabel='v',zlabel='vis phase')



# ug = np.load(path+'gridded-u0.npy')
# vg = np.load(path+'gridded-v0.npy')
# ug = ug.flatten()
# vg = vg.flatten()

# visg = np.load(path+'gridded-vis0.npy')
# visg = visg.flatten()

# uvwraw = np.load(path+'uvw0.npy')
# ur = uvwraw[:,0,0]
# vr = uvwraw[:,1,0]

# visr = np.load(path+'vis0.npy')
# visr = visr[:,0]

# data1 = go.Scatter3d(x=ur, y=vr, z=np.angle(visr), mode='markers',marker=dict(size=1, color='red'), name='Raw')

# #! NOTE THE NEGATIVE
# data2 = go.Scatter3d(x=-ug, y=vg, z=np.angle(visg), mode='markers',marker=dict(size=1, color='black'), name='Gridded')

# data = [data1,data2]
# fig = go.Figure(data=data)
# fig.update_layout(scene=dict(
#         xaxis_title='u',
#         yaxis_title='v',
#         zaxis_title='phase'))


## sim-vis-img.py run
# raw
uvwr = np.load(path+'model-uvw.npy')
visr = np.load(path+'model-vis.npy')

visr=visr[:,0]
ur=uvwr[:,0,0]
vr=uvwr[:,1,0]
dr={'x':ur, 'y':vr, 'z':np.angle(visr), 'name':'Raw', 'color':'red'}

#gridded
# unames  =['gridded-u-size-10-res-0.1-wres-0.5.npy', 'gridded-u-size-20-res-0.1-wres-0.05.npy', 'gridded-u-size-175-res-0.5-wres-0.5.npy', 'gridded-u-size-60-res-0.3-wres-0.15.npy']
# vnames  =['gridded-v-size-10-res-0.1-wres-0.5.npy', 'gridded-v-size-20-res-0.1-wres-0.05.npy', 'gridded-u-size-175-res-0.5-wres-0.5.npy', 'gridded-u-size-60-res-0.3-wres-0.15.npy']
# visnames=['gridded-vis-size-10-res-0.05-wres-0.5.npy', 'gridded-vis-size-175-res-0.5-wres-0.5.npy', 'gridded-vis-size-10-res-0.1-wres-0.5.npy', 'gridded-vis-size-5-res-0.01-wres-0.5.npy']
gridded_params=[{'size':10,'res':0.1, 'wres':0.5}, {'size':20,'res':0.1, 'wres':0.05}, {'size':175,'res':0.5, 'wres':0.5}, {'size':60,'res':0.3, 'wres':0.15}]

d1={}
d2={}
d3={}
d4={}
dicts=[d1,d2,d3,d4]
for i in np.arange(len(gridded_params)):
    ug = np.load(path+'gridded-u-size-{}-res-{}-wres-{}.npy'.format(gridded_params[i]['size'],gridded_params[i]['res'],gridded_params[i]['wres'])).flatten()
    vg = np.load(path+'gridded-v-size-{}-res-{}-wres-{}.npy'.format(gridded_params[i]['size'],gridded_params[i]['res'],gridded_params[i]['wres'])).flatten()
    visg=np.load(path+'gridded-vis-size-{}-res-{}-wres-{}.npy'.format(gridded_params[i]['size'],gridded_params[i]['res'],gridded_params[i]['wres'])).flatten()

    dicts[i]['x']=-vg
    dicts[i]['y']=ug
    dicts[i]['z']=-np.angle(visg)
    dicts[i]['name']='Gridded w/ size={} res={} wres={}'.format(gridded_params[i]['size'],gridded_params[i]['res'],gridded_params[i]['wres'])
    dicts[i]['color']='black'

fig=get_nscatters(dr, d1, d2, d3, d4, xlabel='u', ylabel='v', zlabel='vis phase')


fig.write_html(path+'scatters.html')
fig.show()
