 #Copyright (c) 2016 Micorosft Corporation

 #Permission is hereby granted, free of charge, to any person obtaining a copy
 #of this software and associated documentation files (the "Software"), to deal
 #in the Software without restriction, including without limitation the rights
 #to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 #copies of the Software, and to permit persons to whom the Software is
 #furnished to do so, subject to the following conditions:

 #The above copyright notice and this permission notice shall be included in
 #all copies or substantial portions of the Software.

 #THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 #THE SOFTWARE.

 # @author Prasanna Mategaonkar <prasanna@introp.net>
 # @license MIT
 # @copyright (C) 2016 onwards Microsoft Corporation (http://microsoft.com/)

 #This file contains the methods used to validate the input parameters at various places.

def validate_string_param(value, name):
    if not value:
        raise ValueError("The {0} parameter is required".format(name))

    if not isinstance(value, str):
        raise TypeError("The {0} parameter must be of type str".format(name))

def validate_boolean_param(value, name):
    if not value:
        raise ValueError("The {0} parameter is required".format(name))

    if not isinstance(value, bool):
        raise TypeError("The {0} parameter must be of type bool".format(name))