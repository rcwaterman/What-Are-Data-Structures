// Implementing an array in C++... hoping to get a bit lower level here. I would like to be able
// do my own memory allocation and add all of the features of the existing C++ array.

#include <iostream>
#include <array>

class Array {
    // 
    private:

        int size;
        int value;

        int allocate_memory(int arrayLen) {
            int* arr = new int[arrayLen];
        }

        void deallocate_memory(int ptr) {

        }

    public: 
        Array(int init_size, int init_val) 
        : size(init_size), value(init_val) {}

        friend int get_size(const Array& arr) {
            return arr.size;
        }

        int& operator[](size_t index) {
            // Optional: Add bounds checking
            if (index >= size) {
                throw std::out_of_range("Index out of range");
            }
            return value[index];
        }

        void display(const Array& arr) const {
            int size = get_size(arr);
            for (size_t i = 0; i < size; ++i) {
                std::cout << "Element " << i << ": " << *arr[i] << std::endl;
            }
        }


};

int main() {

    Array arr(3,1);

    return 0;
}



//This is a working implementation of what I want to do

#include <iostream>
#include <stdexcept>  // Optional: for bounds checking

class Array {
private:
    int* data;
    size_t size;
public:
    // Constructor: allocate an array of given size
    Array(size_t n) : size(n) {
        data = new int[size];
    }
    
    // Destructor: free allocated memory
    ~Array() {
        delete[] data;
    }
    
    // Non-const overload for operator[]
    int& operator[](size_t index) {
        // Optional: Add bounds checking
        if (index >= size) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }
    
    // Const overload for operator[]
    const int& operator[](size_t index) const {
        // Optional: Add bounds checking
        if (index >= size) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }
};

int main() {
    Array arr(10);
    
    // Using non-const operator[] to modify elements
    arr[0] = 42;
    std::cout << "Element at index 0: " << arr[0] << std::endl;
    
    // If you have a const Array, the const version will be used:
    const Array constArr = arr;
    std::cout << "Element at index 0 from const object: " << constArr[0] << std::endl;
    
    return 0;
}
