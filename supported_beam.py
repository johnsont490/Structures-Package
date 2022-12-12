#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from BeamSolver.beam import *

class Supported_Beam(Beam):    
    """
    Creates a customizable beam object, also includes methods to present the Freebody Diagram
    and perform calculations as desired
    """
    
    x_pos = 2.0
    y_pos = 3.0
    p0 = Point(x_pos, y_pos)
    scaled_length= 10
    
    def __init__(self, length, height):
        """
        Initializing the beam properties, additional properties will be added on top
        as the user desires.
        length: [m]
        height: [m]
        """
        self.length = length
        self.height = 1
        self.beam_height = height
        self.main = Rectangle(self.p0, self.scaled_length, height).set_fill_pattern(Style.FillPattern.UP_LEFT_TO_RIGHT)
        self.composition={"main": self.main}
        #self.force_dictionary={}
        self.force_dictionary={'magnitude':[],'position':[],'type':[]}
        #self.moment_dictionary={}
        self.moment_dictionary={'magnitude':[],'position':[],'name':[]}
        #self.support_dictionary={}
        self.support_dictionary={'magnitude':[],'position':[],'type':[]}
        self.UDL_dictionary = {'magnitude':[],'position':[],'distributed_load':[], 'end_position':[]}
        super().__init__(length, height)
        
        self.fixed_support_exist = False
        self.roller_support_exist = False
        
    def fixed_support(self,name,position):
        """
        Adds a fixed support along the beam. This support has reaction forces
        in both the vertical and horizontal directions.
        Only one fixed support can be placed or the problem becomes
        statically indeterminate.
        position: [m]
        """
        
        if self.fixed_support_exist == True:
            raise ValueError("Only one fixed support can exist for the beam to be statically determinate")
        if position>self.length or position<0:
            raise ValueError("Support must be placed on the beam")
        scaled= (position/self.length)*self.scaled_length    
        self.fixed_support_exist=True
        ground_support = SimpleSupport(self.p0 + Point(scaled, 0), self.scaled_length/22)  # pt B is simply supported
        self.support_dictionary['magnitude'].append(None)
        self.support_dictionary['position'].append(position)
        self.support_dictionary['type'].append('fixed')
        self.composition[name] = ground_support
        R1 = Force(f"${name}$",self.p0 + Point(scaled,0) - Point(0, 2 * self.height),ground_support.mid_support)
        R1.set_line_width(3).set_line_color(Style.Color.BLACK)
        self.composition["Fixed_ReactionForce"] = R1
        
    def roller_support(self,name,position):
        """
        Adds a roller support along the beam. This support has reaction forces
        in only the vertical direction.
        As many roller supports can be placed as desired.
        position: [m]
        """
        
        if self.roller_support_exist == True:
            raise ValueError("Only one roller support can exist for the beam to be statically determinate")
        if position>self.length or position<0:
            raise ValueError("Support must be placed on the beam")
        scaled= (position/self.length)*10
        self.roller_support_exist=True
        roller = Circle(self.p0 + Point(scaled, -self.scaled_length/30), self.scaled_length/30)
        self.support_dictionary['magnitude'].append(None)
        self.support_dictionary['position'].append(position)
        self.support_dictionary['type'].append('roller')
        self.composition[name] = roller  
        R2 = Force(f"${name}$",self.p0 + Point(scaled,0) - Point(0, 2 * self.height),roller.center - Point(0,roller.radius))
        R2.set_line_width(3).set_line_color(Style.Color.BLACK)
        self.composition["Roller_ReactionForce"] = R2
    def calculate_forces(self):
        """
        Calculates the support reactions for the beam.
        Solves the system of equations involved from creating a sum of forces,
        and sum of moments.
        """
        if (self.fixed_support_exist != True or self.roller_support_exist!= True):
            raise ValueError("The beam is not static and requires an additional support")
        A=np.ones([2,len(self.support_dictionary['magnitude'])])
        B=np.empty([1,len(self.support_dictionary['magnitude'])])
        force= pd.DataFrame.from_dict(self.force_dictionary)
        moment= pd.DataFrame.from_dict(self.moment_dictionary)
        support = pd.DataFrame.from_dict(self.support_dictionary)
        #Rearranging support dataframe so 'Fixed is always first'
        support= (support.sort_values('type')).reset_index(drop=True)
        fixed_support_position = support['position'][0]
        
        #Fixed Support Position is the beginning of the lever arm. The lever arm
        #is the distance from some force to the fixed support
        #
        sum_force_reactions = -1*force['magnitude'].sum()
        
        #Calculating the moment generated by all forces placed along the beam.
        force['moment'] = (force['position'] - fixed_support_position)*force['magnitude']
        sum_moments_and_couples = -1*force['moment'].sum() - moment['magnitude'].sum()
        
        B[0,0]= sum_force_reactions
        B[0,1] = sum_moments_and_couples
        A[1,0] = 0
        A[1,1] = support['position'][1]
        
        #Solving for support reactions and giving values to the support dictionary.
        support['magnitude']= np.linalg.solve(A, np.transpose(B))
        self.support_dictionary['magnitude'] = list(support['magnitude'])

