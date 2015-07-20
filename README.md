Do you ever get really annoyed by problems of the rough form "shift something representable by an integer along some 
bounded range by some arbitrary integer, then spit out the result?"  For example, the "caesar cipher" that shows up in, like, 
every introductory programming course ever since the beginning of time?

I know I do.  So I've decided to solve it and everything of even remotely similar functional form.  

Usage: 

```
rotate(number, rotateby, top, bottom=0)
```

takes an initial *number* on a scale from *top* to *bottom* (which defaults to 0) and shifts it by *rotateby*.  All of the 
arguments must be integers, and all can be positive or negative, but must satisfy top >= number >= bottom (or it throws a
ValueError).  Top and bottom are both included in the scale.

The mental model you should have here is of an old-school gym locker or combination padlock, where you turn the dial.  Or, of
course, some kind of kids cryptography toy, with the letters  represented by integers.  In fact, I an actual padlock 
in my hand when I wrote this code.  But you can also imagine really dumb padlocks that go from, e.g., -1042 to 20.  It's 
the really dumb stupid ones that make this code surprisingly long (just modulo won't do the trick).

The padlock I had in my hands has 40 ticks, from 0 to 39.  If you have one too, you can try out the following concrete examples:

*start at 5 and rotate back 10 places* is equivalent to ```rotate(5, -10, 39, 0)``` and returns 35.  

*start at 0 and rotate forward 41 places* is equivalent to ```rotate(0, 41, 39, 0)``` and returns 1.  In both cases, the last
argument 0 is optional.

Also supplied in here are ```makeKeyFunction(rotateby, top, bottom=0)``` which is just a closure that returns a rotator 
function tied to those specific parameters, suitable when the same rotation is to be applied to multiple numbers (e.g. in 
encrypting a string); and ```makeRotatorFunction(top, bottom=0)``` which is a similar closure, but returns a function that 
takes both a number and a rotateby --- or, conceptually, the rough equivalent of returning a fixed-length padlock to play 
with.  For example: 

```
foo = makeKeyFunction(-10, 39, 0)
print foo(5)
bar = makeRotatorFunction(39)
print bar(5, -10)
print rotate(5, -10, 39)
```

will just print 35 for each print statement.  

There are also test functions and such.  Testing is simple: uncomment the calls to the test functions and see the joy.

Sooner or later, I'll figure out how to submit a package to pypi, and then this will actually turn into an installable module. 

The code passes all the tests I could cook up for it, but all kinds of bizarre edge cases and off-by-one errors 
seem to like to show up when I start messing around with weird values for the parameters (especially when things go 
negative), and there are a few kind of klugey fixes.  So if you should happen to find a test that breaks it, please do 
file an issue, or just fix it yourself.  


LICENSE BLAH BLAH BLAH
----------------------

The MIT License (MIT)

Copyright (c) 2015 Paul Gowder (http://paul-gowder.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
