
def read_properties(filename):
    import tomli
    from BeamSolver.supported_beam import Supported_Beam
    from BeamSolver.cantilever_beam import Cantilever_Beam
    with open(filename,"rb") as f:
        data = tomli.load(f)
        beam_type = data['type'].lower()
        length= data['length']
        height= data['height']
        if beam_type == 'supported':
            beam= Supported_Beam(length,height)
            fixed_support_iteration = data['fixed_support']
            roller_support_iteration = data['roller_support']
            beam.fixed_support(fixed_support_iteration['name'],fixed_support_iteration['position'])
            beam.roller_support(roller_support_iteration['name'],roller_support_iteration['position'])
                
        elif beam_type == 'cantilever':
            beam = Cantilever_Beam(length,height)
        else:
            raise ValueError('Beam must be supported or cantilever')
        
        
        forces = data.get('forces')
        dist = data.get('UDL')
        moments = data.get('moments')
        
        if forces != None:
            for force in forces:
                force_iteration = forces.get(force)
                name= force_iteration.get('name')
                position = force_iteration.get('position')
                magnitude = force_iteration.get('magnitude')
                beam.point_force(name,position,magnitude)
        if dist != None:
            for loads in dist:
                load_iteration = dist.get(loads)
                name= load_iteration.get('name')
                start = load_iteration.get('start')
                end = load_iteration.get('end')
                distributed_load = load_iteration.get('distributed_load')
                beam.uniform_load(name,start,end,distributed_load)
        if moments != None:
            for moment in moments:
                moment_iteration = moments.get(moment)
                name= moment_iteration.get('name')
                position = moment_iteration.get('position')
                magnitude = moment_iteration.get('magnitude')
                beam.moment(name,position,magnitude)
    return beam
