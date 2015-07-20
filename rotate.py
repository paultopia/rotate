def rotate (number, rotateby, top, bottom=0):
    """shifts an arbitrary integer (NUMBER) by another arbitrary integer
    (ROTATEBY), along an integerrange defined by TOP and BOTTOM.  If range is
    exceeded, flows around like a padlock.  Models, e.g., primitive ciphers.

    Operating with the padlock metaphor, BOTTOM is the lowest digit that appears
    on the padlock, while TOP is the highest digit.  E.g., with an ordinary
    40-number padlock that has ticks from 0-39, bottom=0, top=39.

    This is necessary because trying to implement these things, at least with
    my decaying brain, yields an endless number of off-by-one errors, especially
    around the top and bottom of range, with negative numbers, etc.  So I'm
    just trying to beat the whole mess down with a general solution.  I actually
    had to sit there with a padlock in hand to work this all out.
    """
    if bottom > top:
        raise ValueError('Maximum of range lower than minimum of range')
    if (number > top) or (number < bottom):
        raise ValueError('Starting number out of range')
    if top == bottom:
        return number
    if rotateby > 0:
        if bottom == 0:
            return forward0RT(number, rotateby, top)
        else:
            return forwardXRT(number, rotateby, top, bottom)
    elif rotateby < 0:
        if bottom == 0:
            return back0RT(number, rotateby, top)
        else:
            return backXRT(number, rotateby, top, bottom)
    else:
        return number

def makeRotatorFunction(top, bottom=0):
	"""closure over function to repeatedly rotate based on a given range,
    useful when multiple keys are to be generated based on the same range.
    conceptually, returns a fixed-dimension padlock that you get to toy with.
	actually returns a version of rotate() above with top and bottom fixed.
	"""
	def rotator(number, rotateby):
		return rotate(number, rotateby, top, bottom)
	return rotator

def makeKeyFunction(rotateby, top, bottom=0):
	"""another closure, just like above, except this fixes rotateby and
    top/bottom useful for applying the same rotation to numerous items, e.g.,
    a text to be encrypted by a caesar cipher.
	"""
	def rotator(number):
		return rotate(number, rotateby, top, bottom)
	return rotator

# you probably don't need to worry about any of the sub-functions down below
# unless something breaks.

def forward0RT(number, rotateby, top):
    """This is the normal case, and also easiest to calculate
    """
    realrot = rotateby % (top + 1)
    result = number + realrot
    if result > top:
        result -= top + 1
    return result

def back0RT(number, rotateby, top):
    realrot = rotateby % (top + 1)
    return forward0RT(number, (realrot + top + 1), top)

def forwardXRT(number, rotateby, top, bottom):
    offset = bottom
    unset = forward0RT(number, rotateby, top)
    numrotations = rotateby / (top - bottom)
    if (rotateby + number > top) and (numrotations == 0):
        numrotations += 1
    answer = unset + (offset * numrotations)
    if answer > top:
        answer -= (top + 1)
    return answer


def backXRT(number, rotateby, top, bottom):
    offset = bottom
    unset = back0RT(number, rotateby, top)
    numrotations = abs(rotateby) / (top - bottom)
    if number + rotateby <= 0:
        numrotations += 1
    # the abs is necessary because integer division in python
    # floors rather than truncates.  which is stupid, but there you go.
    answer = unset - (offset * numrotations)
    if answer < bottom:
        answer += (top + 1)
    return answer

def runtests():
    """ obvs uncomment the call to this sucker below to test.  add more
    freakish edge cases as you please.
    """
    print 'TESTING FORWARD ROTATION ON ZERO-BASE'
    print 'should produce 5, produces: ',
    print rotate(0, 5, 39)
    print 'should produce 5, produces: ',
    print rotate(0, 45, 39)
    print 'should produce 5, produces: ',
    print rotate(0, 125, 39)
    print 'should produce 6, produces: ',
    print rotate(1, 125, 39)
    print 'should produce 4, produces: ',
    print rotate(39, 5, 39)
    print 'should produce 4, produces: ',
    print rotate(39, 125, 39)
    print
    print 'TESTING BACKWARDS ROTATION ON ZERO-BASE'
    print 'should produce 35, produces: ',
    print rotate(0, -5, 39)
    print 'should produce 30, produces: ',
    print rotate(35, -5, 39)
    print 'should produce 35, produces: ',
    print rotate(0, -45, 39)
    print 'should produce 30, produces: ',
    print rotate(35, -45, 39)
    print 'should produce 35, produces: ',
    print rotate(0, -125, 39)
    print 'should produce 30, produces: ',
    print rotate(35, -125, 39)
    print 'should produce 0, produces: ',
    print rotate(5, -5, 39)
    print
    print 'TESTING FORWARD ROTATION ON NONZERO BASE'
    print 'should produce 5, produces: ',
    print rotate(0, 5, 39, -1)
    print 'should produce 5, produces: ',
    print rotate(0, 46, 39, -1)
    print 'should produce 5, produces: ',
    print rotate(0, 87, 39, -1)
    print 'should produce 5, produces: ',
    print rotate(0, 128, 39, -1)
    print 'should produce 10, produces: ',
    print rotate(5, 5, 39, -1)
    print 'should produce 10, produces: ',
    print rotate(5, 128, 39, -1)
    print 'should produce 39, produces: ',
    print rotate(0, 39, 39, -1)
    print 'should produce -1, produces: ',
    print rotate(0, 40, 39, -1)
    print 'should produce -1, produces: ',
    print rotate(0, 81, 39, -1)
    print 'should produce 0, produces: ',
    print rotate(0, 82, 39, -1)
    print 'should produce 0, produces: ',
    print rotate(0, 41, 39, -1)
    print 'should produce 10, produces: ',
    print rotate(5, 5, 39, 1)
    print 'should produce 11, produces: ',
    print rotate(5, 45, 39, 1)
    print 'should produce 10, produces: ',
    print rotate(5, 83, 39, 1)
    print 'should produce 2, produces: ',
    print rotate(39, 2, 39, 1)
    print 'should produce 1, produces: ',
    print rotate(39, 1, 39, 1)
    print
    print 'TESTING BACKWARD ROTATION ON NONZERO BASE'
    print 'should produce 36, produces: ',
    print rotate(0, -5, 39, -1)
    print 'should produce 35, produces: ',
    print rotate(1, -5, 39, 1)
    print 'should produce 5, produces: ',
    print rotate(10, -5, 39, 5)
    print 'should produce 35, produces: ',
    print rotate(1, -44, 39, 1)
    print 'should produce 35, produces: ',
    print rotate(1, -83, 39, 1)
    print 'should produce 35, produces: ',
    print rotate(0, -47, 39, -1)
    print 'should produce 35, produces: ',
    print rotate(5, -52, 39, -1)
    print 'should produce 5, produces: ',
    print rotate(10, -5, 39, -1000)
    print 'should produce 35, produces: ',
    print rotate(10, -10, 39, 5)
    print 'should produce 38, produces: ',
    print rotate(1, -2, 39, 1)
    print 'should produce 39, produces: ',
    print rotate(1, -1, 39, 1)
    print
    print 'final test--should produce 5 as default, produces: ',
    print rotate(5, 0, 39, 0)
    # my brain hurts, so this is tested enough.  if you find any incorrect
    # results here in some bizarre edge case, you fix it and send a pull
    # request kthxbye.

#runtests()

def closuretests():
    print 'TESTING ROTATOR CLOSURES'
    print
    print 'TESTING MAKE-KEY FUNCTION'
    rot5 = makeKeyFunction(5, 39)
    print 'should produce 5, produces: ',
    print rot5(0)
    rot10 = makeKeyFunction(-5, 39, 5)
    print 'should produce 5, produces: ',
    print rot10(10)
    rotCY = makeKeyFunction(-10, 39, 5)
    print 'should produce 35, produces: ',
    print rotCY(10)
    print
    print 'TESTING MAKE-ROTATOR FUNCTION'
    rot5b = makeRotatorFunction(39)
    print 'should produce 5, produces: ',
    print rot5b(0, 5)
    print 'should produce 10, produces: ',
    print rot5b(0, 10)
    rot10b = makeRotatorFunction(39, 5)
    print 'should produce 5, produces: ',
    print rot10b(10, -5)



# closuretests()

def errortest1():
    print 'should throw ValueError: out of range'
    print rotate(40, 5, 39)

def errortest2():
    print 'should throw ValueError: out of range'
    print rotate(-1, 5, 39)

def errortest3():
    print 'should throw ValueError: dumb range'
    print rotate(0, 5, 5, 10)

#errortest1()
#errortest2()
#errortest3()
