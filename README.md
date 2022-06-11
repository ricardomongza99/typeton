# 🦭 TYPETON
An object oriented language developed by two rockstar engineering students at Tec de Monterrey.

## ⭐️ FEATURES
- Local and global variables
- Shorthand assign operators (+=, -=, *=, /=)
- Arrays (with primitives)
- Conditionals
- Loops
- Functions
- Classes
- Input/Output

## 🚗 GETTING STARTED

To install dependencies run  ```pip install .```

To run the compiler simply execute ```python3 -m src.main```

To run custom programs, make sure the program is inside the programs folder and run ```python3 -m src.main #program_name```

Add ```-debug``` flag at the end to display extra information such as quads, function data and symbol tables


---
**Start**
```
func main() -> {
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
var i = 0
while (i < 10) {
    print(i)
    i += 1
}
```


**Functions** 
func *name* (*param_name: type*, ...) -> *return type*
```
func sum(num1: Int, num2: Int) -> Int {
    return num1 + num2
}

func main() -> {
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

func main() -> {
    var dog: Animal
    dog = new Dog()
    dog.name = "Albert"
    dog.age = 18
    
    print(dog.name)
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
    var items: Int[5]
    var i: Int
    
    i = 0
    while (i < 5) {
        items[i] = i + 10
        i += 1
    }
    
    i = 0
    while (i < 5) {
        print(items[i])
        i += 1
    }
}
```

**Program 2**: Input
```
func main() {
    var age: Int
    age = input("What is Jason's age?")
    print("Jason's age is ")
    print(age)

    var color: String
    color = input("What is Jason's favorite color?")
    print("Jason's favorite color is...")
    print(color)
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
    - [x] Arrays
    - [x] Classes
- [x] 🖥 Virtual Machine
    - [x] Memory for execution (Global memory, temporal memory, execution stack)
    - [x] Arithmetic expressions execution
    - [x] Sequential blocks execution
    - [x] Conditional blocks execution
- [x] 🏁 Documentation review

## 🔍 SYNTAX DIAGRAM
![Program](/diagram/program.png)
![Top level](/diagram/top_level.png)
![Params](/diagram/params.png)
![Type](/diagram/type.png)
![Blocks](/diagram/blocks.png)
![Classes](/diagram/classes.png)
![Statements](/diagram/statements.png)
![Expressions](/diagram/expressions.png)
![Variables](/diagram/variables.png)
