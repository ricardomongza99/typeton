# 🦭 TYPETON
An object oriented language developed by two undergrads from Tec de Monterrey.

## ⭐️ FEATURES
- Local and global variables
- Classes
- Functions
- Conditionals
- Loops
- Inheritance (one level)
- Input / Output
- String Interpolation
- Arrays (with primitives)
- Implicit types (detects primitives)
- Shorthand assign operators (+=, -=, *=, /=)

## 📝 CODE EXAMPLES
**Program 1**: Compare two numbers
```
func main() {
    var number1 = 20
    var number2 = 30

    if (number1 < number2) {
        print("Number 1 is less than number 2")
    } else {
        print("Number 2 is less than number 1")
    }
}
```

**Program 2**: While loop count from 4 to 10
```
func main() {
    var counter = 4

    while (counter < 10) {
        print(counter)
        counter += 1
    }
}
```

**Program 3**: Iterate over an array of integers
```
func main() {
    var items: [Int] = [1, 2, 3, 4, 5]
    var i = 0

    while (counter < 10) {
        print(items[i])
        i += 1
    }
}
```
**Program 4**: Add function
```
func add(num1: Int, num2: Int) -> Int {
    return num1 + num2
}

func main() {
    var sum = add(2, 5)
    print(sum)

}
```
**Program 5**: Class inheritance
```
class Animal {
    var name: String
    var age: Int

    func sleep() {
        print("\(name) is sleeping")
    }
}

class Dog: Animal {
    var isBig: Bool

    func bark() {
        if (isBig) {
            print("Wooff!")
        } else {
            print("wuf wuf")
        }
    }
}

class Cat: Animal {
    
    func meow() {
        print("Meow")
    }
}

 
func main() {
    var dog1 = Dog("Harold", 12, True)
    var dog2 = Dog("Pinky", 5, False)
    var cat = Cat("Tom", 6)

    var animals: [Animal] = [dog1, dog2, cat]

    for animal in animals {
        animal.sleep()
    }
}
```

