import numpy as np
import random
#import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Utility import *
import Image
import Strokes
import time
import math


def initial_stroke(m_s):                       # Create a stroke with parameters set below.
    length = 100
    width = 20
    color = (100, 100, 200)
    m_s.length = length
    m_s.width = width
    m_s.lists = []
    return m_s


noc=0

class Single_curve(object):
	def __init__(self,up_side, down_side,style,canvas,fig1,im):
		self.up_side=up_side
		self.line_b=up_side.keys()
		self.line_b.sort()
		self.line_d=down_side.keys()
		self.line_d.sort()
		#print "here",len(self.line_b)," ",len(self.line_d)
		self.width=[]  #a list of the width, pass to the stroke
		self.length=[]  #a list of the length, pass to the stroke
		self.color=[] #a list of the color, pass to the stroke
		self.starting_point=[] #a list of starting points, using this point to search the width of per stroke.
		self.ending_point=[] # a list of ending points
		self.starting_point_down=[] #a list of starting points on the down side, using four points we can know where to render.
		self.ending_point_down=[] # # a list of ending points on the down side
		self.style=style

		self.max_len=0 #determined by the style, needed in the get_starting_points function  #done 
		self.min_len=0 #determined by the style, needed in the get_starting_points function  #done
		self.__max_cur=0 #determined by the style, needed in the get_starting_points function
		self.angle=[]
		self.fig1 = fig1
		self.canvas=canvas
		self.im=im
           

		

	def get_lenrange(self): # the max_len, min_len and max_cur are determined by the style
                #average_width=sum(width)/len(width)
                #determine average width
		#width=line_b[0].x
		wid_ar=np.array([self.line_b[0][0]-self.line_d[0][0],self.line_b[0][1]-self.line_d[0][1]])

		l1=np.sqrt(wid_ar.dot(wid_ar))
		wid_ar=np.array([self.line_b[-1][0]-self.line_d[-1][0],self.line_b[-1][1]-self.line_d[-1][1]])
		l2=np.sqrt(wid_ar.dot(wid_ar))
		average_width=(l1+l2)/2

                self.max_len=average_width*5.0#/0.618#/0.618
                self.min_len=average_width*2.0#*0.618
                
	def get_length(self): 
                begin=0
                i=0
                isterminal=0
                
                cur_boundary=0.05236
                while (isterminal==0):
                        span=random.randint(int(float(self.min_len)),int(float(self.max_len)))
			#print (span)
			if begin+span>=(len(self.line_b)-1): #terminal condition
                        	end=len(self.line_b)-1#xX
                        	#end_d=len(self.line_d)-1
                        	isterminal=1
				#print("terminal end")
				#print(end)

                            #self.__ending_point.append(line_b[len(line_b)-1]) #end point include the last point   
                            #break
                        else:
                        	end=begin+span
                             
                        mid=(begin+end)/2
                        direction1=np.array([self.line_b[mid][0]-self.line_b[begin][0],self.line_b[mid][1]-self.line_b[begin][1]])
                        l1=np.sqrt(direction1.dot(direction1))
                        direction2=np.array([self.line_b[end][0]-self.line_b[mid][0],self.line_b[end][1]-self.line_b[mid][1]])
                        l2=np.sqrt(direction2.dot(direction2))
                        if (l1*l2!=0):
				cos_curvature=(direction1.dot(direction2)/(l1*l2))
				#print "cos ",cos_curvdature
				if int(cos_curvature) == 1:
					curvature = 0
				else:
	                        	curvature=np.arccos(cos_curvature)
				#print curvature
			else:
				curvature=0
			#print("the cur is")
			#print(curvature)
                        if (curvature<cur_boundary):
				self.starting_point.append(self.line_b[begin])
                                        #self.starting_point_down.append(self.line_d[begin])
				self.ending_point.append(self.line_b[end])
                                        #self.ending_point_down.append(self.line_d[begin])
				begin=int(end-span*curvature/6/3.1415926)
				
				
                        else:
                                #p=0.8
                                cur_norm=1+curvature/3.1415926 #curvature>1
                                cur_start=begin
				iscurterminal=0
				
				#self.starting_point.append(self.line_b[cur_start])
				while (iscurterminal==0):
					#print cur_norm
                                        cur_span=random.randint(int((self.min_len)/(cur_norm)),int((self.max_len)/(cur_norm)))
					
                                	if (cur_start+cur_span>=end):#terminal condition of cur
						cur_end=end
						iscurterminal=1
						self.starting_point.append(self.line_b[cur_start])
					#self.starting_point_down.append(self.line_d[begin])
						self.ending_point.append(self.line_b[cur_end])
						begin=int(cur_end-cur_span*curvature/(2*3.1415926))
					else:
						cur_end=cur_start+cur_span
						self.starting_point.append(self.line_b[cur_start])
					#self.starting_point_down.append(self.line_d[begin])
						self.ending_point.append(self.line_b[cur_end])
						cur_start=int(cur_end-cur_span*curvature/(2*3.1415926))
                                                   
					
						
	def fortest(self):
		flag=0
		
		for i in range(len(self.starting_point)):
			wid_ar=np.array([self.starting_point[i][0]-self.ending_point[i][0],self.starting_point[i][1]-self.ending_point[i][1]])
			if((self.starting_point[i][1]-self.ending_point[i][1])>0):
				flag=1
			else:
				flag=0
			l1=np.sqrt(wid_ar.dot(wid_ar))
			self.length.append(l1)
			direction1=np.array([self.ending_point[i][0]-self.starting_point[i][0],self.ending_point[i][1]-self.starting_point[i][1]])
			l1=np.sqrt(direction1.dot(direction1))
			direction2=np.array([1,0])
                        l2=np.sqrt(direction2.dot(direction2))
			if (l1*l2!=0):
                        	cos_curvature=(direction2.dot(direction1)/(l1*l2))
			else:
				cos_curvature=0			

                        curvature=np.arccos(cos_curvature)
			if (flag==0):
				self.angle.append(curvature*57.29)
			else:
				self.angle.append(-curvature*57.29)
			

	def get_width(self):
		begin=0
		for point in self.starting_point:
			wid_ar=np.array([point[0]-self.line_d[begin][0],point[1]-self.line_d[begin][1]])
			min_len=np.sqrt(wid_ar.dot(wid_ar))
			min_pt=self.line_d[begin]
			for point_under in self.line_d[begin:]:
				wid_ar=np.array([point[0]-point_under[0],point[1]-point_under[1]])
				l1=np.sqrt(wid_ar.dot(wid_ar))
				if l1<min_len:
					min_len=l1
					min_pt=point_under
			#the min_len is pass to the stroke, and 
			self.starting_point_down.append(min_pt)
			self.width.append(min_len)
		pass
#get the coordinate of the up_side and down side of
                                             #the curve and the point it is going to spilt the
					     #curve in to different pieces.

#get_color in other parts should be public, I can use it to fullfill my list of color.
	
	def render(self):
		#global noc
		#noc+=1
		#print 'Curve',noc
		self.get_lenrange()
		self.get_length()
		self.get_width()
		self.fortest()
		#fig1 = plt.figure()
		'''
		ax1 = self.fig1.add_subplot(111, aspect='equal')
		ax1.set_xlim(-1,200)
		ax1.set_ylim(-1,200)
		for i in range(len(self.starting_point)):
			p=patches.Rectangle(
        		(self.starting_point[i][0],self.starting_point[i][1]),   # (x,y)
        		self.length[i],          # width
        		-(self.width[i]),          # height
			angle=self.angle[i]
			)
			ax1.add_patch(p)
		'''
		#fig1.show()
		#fig1.savefig('rect2.png', dpi=90, bbox_inches='tight')
		self.middle_start=[]
		self.middle_end=[]
		for i in range(len(self.starting_point)):
			self.middle_start.append((int((self.starting_point[i][0]+self.starting_point_down[i][0])/2),int((self.starting_point[i][1]+self.starting_point_down[i][1])/2)))
			self.middle_end.append((self.middle_start[i][0]+(self.ending_point[i][0]-self.starting_point[i][0]),self.middle_start[i][1]+(self.ending_point[i][1]-self.starting_point[i][1])))
##test

		#im = Image.new("RGB", (400, 400), (255, 255, 255))
		'''for i in range(19):
    			k = 20*(i+1)
   			for j in range(400):
        			im.putpixel((k, j),(0, 0, 0))
        			im.putpixel((j, k), (0, 0, 0))'''

		s = Strokes.Stroke()
		s = initial_stroke(s)

# Here you can revise these parameters according to the introduction in the Strokes Class.
		s.distort = 0.6
		s.shake = 0.6
		s.tapering = 0.7
		s.ColorVariability = 0.8
		s.ShadeVariability = 0.8

		for i in range(len(self.middle_start)):
			# c=Strokes.Color(0,255,0)
			c = Strokes.Color(self.up_side[self.starting_point[i]][0], self.up_side[self.starting_point[i]][1],
							  self.up_side[self.starting_point[i]][2])
			s.color = c
			# print "width",self.width[i]
			if self.middle_start[i][0] != self.middle_end[i][0] and self.middle_start[i][1] != self.middle_end[i][1]:
				points = s.draw_strokes(self.im, self.middle_start[i][0], self.middle_start[i][1],
										self.middle_end[i][0], self.middle_end[i][1], self.width[i], s.color)
				# print "test: ",self.middle_start[i][0],self.middle_start[i][1],self.middle_end[i][0],self.middle_end[i][1]
				# print "points len",len(points)
				for j in range(len(points)):
					p = points[j]
					c = p[2]
					# self.im.putpixel((sself.middle_start[0][0]-s.length/2+p[0],self.middle_start[0][1]+p[1]),c.get_color())
					old_color = self.canvas[self.middle_start[i][0] + p[0]][self.middle_start[i][1] + p[1]][0:3]
					old_alpha = self.canvas[self.middle_start[i][0] + p[0]][self.middle_start[i][1] + p[1]][3]
					new_color = np.array(c.get_color())
					new_alpha = 0.8
					final_color, final_alpha = merge(new_color, old_color, new_alpha, old_alpha)
					self.canvas[self.middle_start[i][0] + p[0]][self.middle_start[i][1] + p[1]][0:3] = final_color
					self.canvas[self.middle_start[i][0] + p[0]][self.middle_start[i][1] + p[1]][3] = final_alpha

				#print "pos ",200+p[0],200+p[1]
			#self.im.show()

		#pass
#using the class of stroke, get the location of the stroke using four points. Details are TBD.




