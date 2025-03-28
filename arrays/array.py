"""
In this file we will implement our own array. In attempt to better understand this at a lower level, the ctypes 
package will be used for manual memory allocation.
"""

import ctypes

class Array():
    """
    So, I know that lists (or arrays) are iterable, can be indexed, added to, or removed from.

    Let's implement these.

    NOTE: This is a very pythonic implementation. I am allowing for mixed types to retain the functionality that exists
    in python lists. I will do a true array implementation in C++ as well.
    """

    def __init__(self, element=None, unpack=True):
        """
        We will probably want this to init with whatever is passed into the array as a valid element.

        If nothing is passed to the array, initialize with the capacity for one element.

        By default, the array will unpack lists or other arrays that are initialized within it.
        """

        self.length = 0
        self.elements = 0
        self.array = self.allocate_array()

        # if there is an element passed, see if it is iterable, otherwise, handle it
        if element is not None:
            #check if the element is a list... if so, unpack into our array
            if isinstance(element,list) or isinstance(element,Array):
                if unpack:
                    self.array = self.allocate_array(len(element))
                    for i in range(len(element)):
                        self.array[i] = element[i]
                        self.length+=1
                #otherwise, dump the element into an element
                else:
                    self.append(element, unpack=False)
            else:
                self.append(element)

    def __len__(self) -> int:
        """
        Return the length of the array. 
        """
        return self.length
    
    def __getitem__(self, index):
        """
        Get an element by it's index.
        """
        if not 0 <= index < self.elements:
            raise IndexError('Index out of bounds')
        return self.array[index]
    
    def __str__(self):
        array_str = "["
        if len(self.array):
            for i in range(len(self.array)):
                array_str = array_str + str(self.array[i]) + ', '
            array_str = array_str[:-2] + ']'
        else:
            array_str = array_str + ']'
        return array_str

    def allocate_array(self, element_count=None):
        """
        Allocate the memory required for this array.
        """
        if element_count is not None:
            self.elements = element_count
        return (self.elements * ctypes.py_object)()
    
    def _resize(self, new_element_count):
        """
        The resize function is an internal method that is called when adding or removing elements.
        """
        temp = self.allocate_array(new_element_count)
        for i in range(len(self.array)):
            temp[i] = self.array[i]
        self.array = temp
        self.length = new_element_count

    def append(self, element, unpack=False):
        """
        This function will always take in an element and assign the index based on the size of the existing array. 

        It is important to note that the index of the last element will always be 1-length.

        This also needs to handle list inputs, which will be unpacked based on the unpack keyword.
        """
        
        #check if the element is a list... if so, unpack into our array
        if isinstance(element,list) or isinstance(element,Array):
            if unpack:
                self.original_length = self.length
                self._resize(self.length + len(element))
                for i in range(len(element)):
                    self.array[self.original_length+i] = element[i]
            else:
                self.length+=1
                self._resize(self.length)
                self.array[self.length-1] = element
        else:
            self.length+=1
            self._resize(self.length)
            self.array[self.length-1] = element

    def insert(self, element=None, index=0, unpack=False):
        """
        Place the element into the array at a given index.

        The default behavior is to place the element at index 0.

        The unpack keyword will unpack the element at the index if it is a list.
        """

        # I want to simulate how this would be done at the lowest level, which is to inject the value
        # at index zero, then shift all subsequent values

        #check if the element is a list... if so, unpack into our array
        if isinstance(element,list) or isinstance(element,Array):
            if unpack:
                self.original_length = self.length
                self._resize(self.length + len(element))
                for i in range(len(element)):
                    # The value should only be inserted if we are at the defined index
                    if i < index + len(element):
                        self.array[self.original_length+i] = element[i]
            else:
                self.length+=1
                self._resize(self.length)
                self.array[self.length-1] = element
            
        else:
            self.length+=1
            self._resize(self.length)
            self.array[self.length-1] = element

    def pop(self, index=None):
        """
        Remove an item based on it's index. Default is to remove the last item.
        """
        if index is None:
            tmp = self.array[0:-1]
            self.array=tmp
            self._resize(self.length-1)
        else: 
            if index > 0:
                tmp = self.array[0:index-1]
                for i in range(len(self.array[index::])):
                    tmp.append(self.array[index+i])
                self.array=tmp
                self._resize(self.length-1)
            else:
                tmp = self.array[1::]
                self.array=tmp
                self._resize(self.length-1)

if __name__ == '__main__':
    array1 = Array([(1,2,3,4,5,6), (1,2,3,4,5,6)], unpack=False)
    print(array1, len(array1))
    array1.insert([6,7,8,9,10], unpack=True)
    print(array1, len(array1))
    array2 = Array(2)
    print(array2, len(array2))
    array1.append(array2)
    print(array1, len(array1))
