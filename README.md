# 🦭 TYPETON
An object oriented language developed by two rockstar engineering students at Tec de Monterrey.

## ⭐️ FEATURES
- Local and global variables
- Shorthand assign operators (+=, -=, *=, /=)
- String Interpolation
- Arrays (with primitives)
- Conditionals
- Loops
- Functions
- Classes
- Input/Output

## 🚗 GETTING STARTED

To install dependencies simply run  ```pip install .```

To run the compiler simply execute ```python3 -m src.main```

To Execute Specific Files: ```python3 -m src.{directory}.{fileName}```

---
**Start**
```
func main() {
    // Program starts here
}
```

**Variable declaration**
```
var myString: String
var myNumber: Int
var myDog: Dog
```


**Arrays**
```
var items: Int[10]
items[0] = 1

var Cube: Int[4][4][4]
cube[1][2][3] = 10
```


**Conditionals**
```
if ( 4 + 1 < 5 && true) {
    print("First")
} else if (2 == 3) {
    print("Second")
} else {
    print("Third")
}
```

**Loops**
```
var counter = 4

while (counter < 10) {
    print(counter)
    counter += 1
}
```


**Functions** 
func *name* (*param_name: type*, ...) -> *return type*
```
func sum(num1: Int, num2: Int) -> Int {
    return num1 + num2
}

func main() {
    var sum = sum(5, 2)
}
```

**Classes**
```
class Animal {
    // Declare properties
    name: String
    age: Int
}
```

**Input**
```
age = input("Enter age: ")
```

**Output**
```
print(userAge)
```


## 👨‍💻 CODE EXAMPLES


**Program 1**: Iterate over an array of integers
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

**Program 2**: Class inheritance
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
    
    var existed: String = ""
    if (dog1.age < dog2.age) {
        existed = "younger"
    } else {
        existed = "older"
    }
    
    print("\(dog1.name) is \(existed) than \(dog2.name)")

}
```

## 📝 TODO
- [x] 💍 Project proposal
    - [x] Documentation
    - [x] Syntax diagram
- [x] 🪙 Lexical analysis
- [x] 📖 Syntax analysis
- [x] 🧠 Semantic analysis
    - [x] Functions directory
    - [x] Variable tables
    - [x] Semantics cube
    - [x] Heap Allocator
- [ ] 🏭 Code generation 
    - [x] Arithmetic expressions
    - [x] Short Hand Assignments (+=, -=, *=, /=)
    - [x] Sequential blocks (ASSIGN, INPUT, ETC.)
    - [x] Conditional blocks (IF, ELSE, WHILE, WHILE)
    - [x] Functions
    - [ ] Arrays
    - [ ] Classes
    - [ ] Objects
- [x] 🖥 Virtual Machine
    - [x] Memory for execution (Global memory, temporal memory, execution stack)
    - [x] Arithmetic expressions execution
    - [x] Sequential blocks execution
    - [x] Conditional blocks execution
- [ ] 🏁 Documentation review

## 🔍 SYNTAX DIAGRAM
![Program](/diagram/program.png)
![Top level](/diagram/top_level.png)
![Params](/diagram/params.png)
![Blocks](/diagram/blocks.png)
![Statements](/diagram/statements.png)
![Expressions](/diagram/expressions.png)
![Variables](/diagram/variables.png)
