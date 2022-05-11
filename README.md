# 🦭 TYPETON
An object oriented language developed by two rockstar engineering students at Tec de Monterrey.

## ⭐️ FEATURES
- Local and global variables
- Implicit types (detects primitives)
- Shorthand assign operators (+=, -=, *=, /=)
- String Interpolation
- Arrays (with primitives)
- Conditionals
- Loops
- Functions
- Classes
- Inheritance (one level)
- Input/Output

## 🚗 GETTING STARTED
**Start**
```
func main() {
    // Program starts here
}
```

**Variables**
```
var myString: String = "Hello world!"
var myNumber: Int = 5
var myDog: Dog = Dog("Draco", 8)
```

**Implicit variables** (only for primitive types)
```
var myDecimal = 5.23
```

**Arrays**
```
var items: [Int] = [1, 2, 3, 4, 5]
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
    var name: String
    var age: Int
    
    // Declare methods
    func sleep() {
        print("\(name) is sleeping")
    }
}
```

**Input**
```
var userAge: Int = input()
```

**Output**
```
print(userAge)
```

**String Interpolation**
```
print("You are \(userAge) years old!")
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
    - [ ] Variable tables
    - [x] Semantics cube
- [ ] 🏭 Code generation 
    - [ ] For arithmetic expressions
    - [ ] For sequential blocks (ASSIGN, INPUT, ETC.)
    - [ ] For conditional blocks (IF, ELSE, WHILE)
    - [ ] For functions
    - [ ] For arrays
    - [ ] For objects
- [ ] 🖥 Virtual Machine
    - [ ] Memory for execution (Global memory, temporal memory, execution stack)
    - [ ] Arithmetic expressions execution
    - [ ] Sequential blocks execution
    - [ ] Conditional blocks execution
- [ ] 🏁 Documentation review

## 🔍 SYNTAX DIAGRAM
![Program](/diagram/program.png)
![Top level](/diagram/top_level.png)
![Params](/diagram/params.png)
![Blocks](/diagram/blocks.png)
![Statements](/diagram/statements.png)
![Expressions](/diagram/expressions.png)
![Variables](/diagram/variables.png)
