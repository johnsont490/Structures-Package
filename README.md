# PythonProject
A statics/structures package that can solve general problems and automatically generate beam illustrations and shear force/bending moment diagrams.


## Beam Solver Module
The beam solver module is a tool for solving statically determinate beams. The beams are restricted to supported and cantilever arrangements.
Beams are initially defined as either a Support_Beam or Cantilever_Beam object. Methods exist within the object to construct the features
and reactions acting upon the beam. The beam and it's reactions can then be solved through methods within the object.

Beams can be constructed from scratch using all the object methods or a read_properties function can be used to read a configuration file, with 
the details of the beam.


### Inputs:

**Point Force**:
* position (m)
* magnitude (N)

**Uniform Distributed Load**:
* start/end (m)
* distributed load (N/m)

**Moment**:
* position (m)
* magnitude (Nm)

**Supports**:
* position (m)

#### Outputs:
**Shear Force / Bending Moment Beam Diagrams**
  * position (m)
  * shear force (N) moment (Nm)

*All attributes of the beam object can also be saved as variables for any further personal calculations*
