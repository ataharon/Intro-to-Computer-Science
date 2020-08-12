# Converted into Python by Prof. Alan Broder from the code found at
# http://cobweb.cs.uga.edu/~maria/classes/4070-Spring-2017/Adam%20Brookes%20Elastic%20collision%20Code.pdf


def PLUS(p, q):  return [p[0]+q[0], p[1]+q[1]]

def MINUS(p, q): return [p[0]-q[0], p[1]-q[1]]

def TIMES(p, c): return [c*p[0], c*p[1]]

def NORMALIZE(p):return TIMES(p, 1/((p[0]*p[0] + p[1]*p[1]) ** 0.5)) 

def DOT(p, q):   return p[0]*q[0] + p[1]*q[1]

# Move each ball back one step before proceding

# assume each ball is a list of at least 4 positions. 
# the first four positions are x, y, dx, dy

def collide(ball1, ball2):
    b1Pos = ball1[0:2]
    b1Vel = ball1[2:4]
    b2Pos = ball2[0:2]
    b2Vel = ball2[2:4]
    
    # Move each ball back one step before proceding
    # Otherwise, the balls might have intersected
    b1Pos = MINUS(b1Pos, b1Vel)
    b2Pos = MINUS(b2Pos, b2Vel)
    
    # Compute the normal vector
    normalVector = MINUS(b2Pos, b1Pos)
    normalVector = NORMALIZE(normalVector)
    
    # Compute the tangent vector
    tangentVector = [-normalVector[1], normalVector[0]] 
    
    # Create ball scalar normal direction
    ball1ScalarNormal = DOT(normalVector, b1Vel)
    ball2ScalarNormal = DOT(normalVector, b2Vel)
    
    # Create scalar velocity in the tangential direction
    ball1ScalarTangential = DOT(tangentVector, b1Vel)
    ball2ScalarTangential = DOT(tangentVector, b2Vel)
    
    ball1ScalarNormalAfter = ball2ScalarNormal
    ball2ScalarNormalAfter = ball1ScalarNormal
    
    ball1scalarNormalAfter_vector = TIMES(normalVector, ball1ScalarNormalAfter)
    ball2scalarNormalAfter_vector = TIMES(normalVector, ball2ScalarNormalAfter)
    ball1ScalarNormalVector = TIMES(tangentVector, ball1ScalarTangential)
    ball2ScalarNormalVector = TIMES(tangentVector, ball2ScalarTangential)
    
    b1Vel = PLUS(ball1ScalarNormalVector, ball1scalarNormalAfter_vector)
    b2Vel = PLUS(ball2ScalarNormalVector, ball2scalarNormalAfter_vector)
    
    # NOW NEED TO PLUG b1Vel AND b2Vel back into the ball descriptors that got passed in
    ball1[2] = b1Vel[0]
    ball1[3] = b1Vel[1]
    ball2[2] = b2Vel[0]
    ball2[3] = b2Vel[1]

    
