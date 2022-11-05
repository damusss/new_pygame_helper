import pygame
from .geometry.lines import Segment

"""Contains the grids classes and some examples."""

cell_grid_color_rules_exaple:dict[int,str|tuple[int,int,int]|pygame.Color] = {0:"white",1:"black"}
"""Example of the cell grid color rules."""
cell_grid_matrix_example:list[list[int]] = [
        [0,0,0,0,1,0,0,0],
        [0,0,1,1,1,1,0,0]
    ]
"""Example of the cell grid matrix."""

class CellGrid:
    """An optimised grid made of cells."""
    matrix_example:list[list[int]] = cell_grid_matrix_example
    """Example of the cell grid matrix."""
    color_rules_exaple:dict[int,str|tuple[int,int,int]|pygame.Color] = cell_grid_color_rules_exaple
    """Example of the cell grid color rules."""
    def __init__(self,topleft_pos:tuple[int,int]|pygame.Vector2,matrix:list[list[int]],cell_size:int,color_rules:dict[int,str|tuple[int,int,int]|pygame.Color]):
        self.topleft_pos:pygame.Vector2= pygame.Vector2(topleft_pos)
        """The position of the grid. <get, set>"""
        self.matrix:list[list[int]] = matrix
        """The number matrix. <get>"""
        self.cell_size:int = cell_size
        """The size of a cell. <get>"""
        self.color_rules:dict[int,str|tuple[int,int,int]|pygame.Color] = color_rules
        """The color rules dict. <get>"""
        x_cell_num = len(self.matrix[0])
        y_cell_num = len(self.matrix)
        self.width:int = x_cell_num*self.cell_size
        """The total width of the grid. <get>"""
        self.height:int = y_cell_num*self.cell_size
        """The total height of the grid. <get>"""
        self.surface:pygame.Surface = pygame.Surface((self.width,self.height))
        """The surface with the cell blitted. <get>"""
        self.refresh_surface()
                
    def refresh_surface(self)->None:
        """Re-draws the cells if something changed."""
        self.surface.fill("black")
        s = pygame.Surface((self.cell_size,self.cell_size))
        for l_i,l in enumerate(self.matrix):
            for n_i,n in enumerate(l):
                color = self.color_rules[n]
                s.fill(color)
                self.surface.blit(s,(n_i*self.cell_size,l_i*self.cell_size))
                
    def draw(self,surface:pygame.Surface)->None:
        """Draws the grid."""
        surface.blit(self.surface,self.topleft_pos)
    
class LineGrid:
    """An optimised grid made of intersecting lines."""
    def __init__(self,topleft_pos:tuple[int,int]|pygame.Vector2,width:int,height:int,cell_size:int,lines_color:str|tuple[int,int,int]|pygame.Color="white",lines_thicness:int=2,force_close_borders:bool=True):
        self.topleft_pos:pygame.Vector2 = pygame.Vector2(topleft_pos)
        """The position of the grid. <get, set>"""
        self.width:int = width
        """The width of the grid. <get>"""
        self.height:int = height
        """The widt of the grid. <get>"""
        self.cell_size = cell_size
        """The size of a cell. <get>"""
        self.color:str|tuple[int,int,int]|pygame.Color = lines_color
        """The color of the lines. <get>"""
        self.thicness:int = lines_thicness
        """The thicness of the lines. <get>"""
        self.segments:list[Segment] = []
        """The list of segments. <get>"""
        self.close_borders:bool = force_close_borders
        """Wheather the borders are closed even if a perfect square can't be made."""
        self.create_segments()
        self.surface:pygame.Surface = pygame.Surface((self.width+self.thicness,self.height+self.thicness))
        """The main surface. <get>"""
        self.refresh_surface()
        
    def create_segments(self)->None:
        """Fill the segments list. Called automatically on the init. Useful if some values changed."""
        self.segments.clear()
        x_lines = self.width//self.cell_size
        y_lines = self.height//self.cell_size
        for y in range(y_lines+1):
            start = (0,y*self.cell_size)
            end = (self.width,y*self.cell_size)
            s = Segment(start,end,self.color,self.thicness)
            
            self.segments.append(s)
            
        if self.close_borders:
            self.segments.append(Segment((0,self.height-self.thicness),(self.width,self.height-self.thicness),self.color,self.thicness))
        
        for x in range(x_lines+1):
            start = (x*self.cell_size,0)
            end = (x*self.cell_size,self.height)
            s = Segment(start,end,self.color,self.thicness)
            self.segments.append(s)
            
        if self.close_borders:
            self.segments.append(Segment((self.width-self.thicness,0),(self.width-self.thicness,self.height),self.color,self.thicness))
            
    def refresh_surface(self)->None:
        """Re-draws the lines in the surface."""
        self.surface.fill("black")
        for s in self.segments:
            s.draw(self.surface)
            
    def draw(self,surface:pygame.Surface)->None:
        """Draws the grid."""
        surface.blit(self.surface,self.topleft_pos)
