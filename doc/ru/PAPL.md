# ru/ PAPL: Programming and Programming Languages

https://papl.cs.brown.edu/2020/

(c) Shriram Krishnamurthi, Benjamin S. Lerner, Joe Gibbs Politz, Kathi Fisler

Книга отличается от PLAI использованием хост-языка `Pyret`, который по своей
модели языка достаточно близок к Python. Начинать предпочтительнее с этой книги,
так как она проще чем [SICP](md_doc_ru_SICP.html).

Этот текст не перевод, а скорее конспект -- будет переведена только очень
небольшая часть текста, которая интересна с точки зрения адаптации к `metaL`.
Читать с листа не очень интересно, так как быстро забывается, конспектирование с
переводом дает лучшее погружение в материал. Возможно вы тоже найдете что-то
интересное для себя, и откроете оригинал чтобы прочитать что там реально
написано. Позднее, и только при условии что `metaL` каким-то чудом взлетит
дальше моих экспериментов, этот текст возможно будет использован для написания
собственного варианта учебника по языку, но шансы на это стремяться к минус
нулю.

# 1 Введение

##      1.1 Наша философия

Многие предпочли бы видеть здесь две книги, а не одну. Первая книга это введение
в программирование, обучающее вас основным концепциям организации данных и
программ, которые с ними работают, и заканчивающееся рассмотрением полезных
универсальных алгоритмов. Другая книга представляет собой введение в языки
программирования: изучение, начиная верхнего уровня, средств с помощью которых
мы структурируем эти данные и программы.

Очевидно, что это не две отдельные темы. Мы изучаем программирование на одном
или нескольких языках, и программы, которые мы пишем, становятся естественными
предметами изучения для понимания языков в целом. Тем не менее, эти темы
считаются достаточно разными, поэтому к ним подходят отдельно. Мы рассматриваем
их таким же образом.

Единственным великим исключением из такого разделения является лучшая из
когда-либо написанных книг по информатике «Структура и интерпретация
компьютерных программ». Мы пришли к выводу, что это разделение не имеет смысла и
не помогает. Темы глубоко переплетены, и если специально допустить их
чередование, то, вероятно, получится гораздо лучшая книга. Это мой эксперимент с
таким форматом. (c) Shriram Krishnamurthi, Benjamin S. Lerner, Joe Gibbs Politz,
Kathi Fisler

##      1.2 Предсказуемость как тема

Есть много способов организовать изучение языков и приёмов программирования. Моя
центральная тема -- концепция предсказуемости.

Программы обычно статичны: они записаны на неком эквиваленте листа бумаги,
неподвижны и неизменны. Но когда мы запускаем программу, она создает сложное,
динамичное поведение, приносящее пользу, удовольствие и (иногда) разочарование.
Каждый, кто пишет программы, в конечном итоге заботится -- осознают он это или
нет -- о необходимости предсказуемого поведения, легко видимого из записи
программы. Иногда мы даже пишем специальные программы, которые помогают нам с
этой задачей (как мы увидим позже).

Предсказуемость имеет плохую репутацию. Под видом научной темы «рассуждений о
поведении программ» это стало рассматриваться одновременно как благородное и
невероятно скучное дело. Это, безусловно, уважаемо, но мы надеемся представить
эти методы так, чтобы они казались совершенно естественными, действительно
совершенно очевидными (потому что мы считаем, что это так). Надеюсь, вы вынесете
из этого учебного курса спокойную уверенность в том, что предсказуемость
занимает центральное место и в вашей собственной работе, и как метрика для
проектирования языков программирования.

##      1.3 Структура книги

В отличие от некоторых других учебников, этот не следует повествованию сверху
вниз. Скорее, это поток обсуждения с возвратами. Мы часто будем создавать
программы пошагово, как это сделала бы пара программистов. Мы будем специально
делать ошибки не потому, что не знаем как правильно, а потому, что для вас это
лучший способ учиться. Включение ошибок делает невозможным пассивное чтение:
вместо этого вы должны взаимодействовать с материалом, потому что вы никогда не
можете быть уверены в правдивости того, что читаете.

В конце вы всегда получите правильный ответ. Однако этот нелинейный путь в
краткосрочной перспективе вызывает большее разочарование (у вас часто возникает
соблазн сказать: «Просто скажите мне уже ответ!»), и он делает книгу плохим
справочником (вы не можете открыть книгу на случайной странице и быть уверены,
что там написано правильно). Однако это чувство разочарования -- это ощущение
реального обучения. Мы не знаем способа обойти это.

В разные моменты вы столкнетесь с этим:
```
Упражнение:
Это упражнение. Попробуйте сделать это.
```

Это традиционное упражнение из учебника. Это то, что вам нужно делать
самостоятельно. Если вы используете эту книгу как часть учебного курса, скорее
всего это будет задано как домашнее задание. Напротив, вы также найдете вопросы,
похожие на упражнения, которые выглядят следующим образом:
```
Делай сейчас!
Здесь нужна ваша активность! Вы видите это?
```

Когда вы доберетесь до одного из них, **остановитесь**. Прочтите, подумайте и
сформулируйте ответ, прежде чем продолжить. Вы должны сделать это, потому что на
самом деле это упражнение, но ответ уже есть в книге -- чаще всего в тексте,
который следует сразу же (то есть в той же части, которую вы сейчас читаете) --
или это то, что вы можете увидеть после запуска программы. Если вы просто
продолжите читать, вы увидите ответ, даже не задумываясь (или не увидев его
вообще, если инструкции предназначены для запуска программы), поэтому вы не
сможете ни (а) проверить свои знания, ни (б) улучшить свою интуицию. Другими
словами, это дополнительные, явные попытки поощрения активного обучения. Однако
в конечном итоге мы можем только предложить эти упражнения; вам решать, будете
ли вы их практиковать.

##      1.4 Язык использованный в книге

В этой книге используется новый язык программирования `Pyret`. Pyret -- это
результат нашего глубокого опыта программирования и проектирования
функциональных, объектно-ориентированных и скриптовых языков, а также их систем
типов, анализа программ, и сред разработки.

Синтаксис языка основан на Python. В отличие от Python, `Pyret` будет требовать
правильные отступы, а не интерпретировать их: то есть отступ просто станет еще
одним критерием проверки синтаксиса. Но это еще не реализовано.

Pyret заполняет нишу, отсутствующую в образовании по информатике, -- простого
языка, который избавляет от странных заморочек Python (которых много), добавляя
важные функции, которых в Python не хватает для обучения программированию
(например, алгебраические типы данных, дополнительные аннотации к переменным,
дизайн языка который позволяют создавать более удобные среды разработки, и
сильная поддержка тестирования). Начинающие программисты могут не напрягаться в
получении знаний, о которых они беспокоятся, в то время как программисты,
которые в прошлом были знакомы с языковым зверинцем, от змей до дромадеров,
должны найти `Pyret` знакомым и удобным.


#    2 Благодарности


#    3 Начала

##      3.1 Мотивирующий пример: флаги

##      3.2 Числа

##      3.3 Выражения

##      3.4 Терминология

##      3.5 Строки

##      3.6 Изображения

###        3.6.1 Комбинация изображений

###        3.6.2 Делаем флаг

##      3.7 Шаг назад: типы, ошибки и документация

###        3.7.1 Типы и контракты

###        3.7.2 Ошибки формата и записи

###        3.7.3 Поиск других функций: документация


#    4 Naming Values

##      4.1 The Definitions Window

##      4.2 Naming Values

###        4.2.1 Names Versus Strings

###        4.2.2 Expressions versus Statements

##      4.3 Using Names to Streamline Building Images


#    5 From Repeated Expressions to Functions

##      5.1 Example: Similar Flags

##      5.2 Defining Functions

###        5.2.1 How Functions Evaluate

###        5.2.2 Type Annotations

###        5.2.3 Documentation

##      5.3 Functions Practice: Moon Weight

##      5.4 Documenting Functions with Examples

##      5.5 Functions Practice: Cost of pens


#    6 Conditionals and Booleans

##      6.1 Motivating Example: Shipping Costs

##      6.2 Conditionals: Computations with Decisions

##      6.3 Booleans

###        6.3.1 Other Boolean Operations

###        6.3.2 Combining Booleans

##      6.4 Asking Multiple Questions

##      6.5 Evaluating by Reducing Expressions

##      6.6 Wrapping up: Composing Functions


#    7 Introduction to Tabular Data

##      7.1 Creating Tabular Data

##      7.2 Processing Rows

###        7.2.1 Keeping

###        7.2.2 Ordering

###        7.2.3 Combining Keeping and Ordering

###        7.2.4 Extending

###        7.2.5 Transforming, Cleansing, and Normalizing

###        7.2.6 Selecting

###        7.2.7 Summary of Row-Wise Table Operations


#    8 From Tables to Lists

##      8.1 Basic Statistical Questions

##      8.2 Extracting a Column from a Table

##      8.3 Understanding Lists

###        8.3.1 Lists as Anonymous Data

###        8.3.2 Creating Literal Lists

##      8.4 Operating on Lists

###        8.4.1 Built-In Operations on Lists

###        8.4.2 Combining Lists and Tables


#    9 Processing Lists

##      9.1 Making Lists and Taking Them Apart

##      9.2 Some Example Exercises

##      9.3 Structural Problems with Scalar Answers

###        9.3.1 my-len: Examples

###        9.3.2 my-sum: Examples

###        9.3.3 From Examples to Code

##      9.4 Structural Problems with List Answers

###        9.4.1 my-str-len: Examples and Code

###        9.4.2 my-pos-nums: Examples and Code

###        9.4.3 my-alternating: First Attempt

###        9.4.4 my-running-sum: First Attempt

##      9.5 Structural Problems with Sub-Domains

###        9.5.1 my-max: Examples

###        9.5.2 my-max: From Examples to Code

###        9.5.3 my-alternating: Examples and Code

##      9.6 More Structural Problems with Scalar Answers

###        9.6.1 my-avg: Examples

##      9.7 Structural Problems with Accumulators

###        9.7.1 my-running-sum: Examples and Code

###        9.7.2 my-alternating: Examples and Code

##      9.8 Dealing with Multiple Answers

###        9.8.1 uniq: Problem Setup

###        9.8.2 uniq: Examples

###        9.8.3 uniq: Code

###        9.8.4 uniq: Reducing Computation

###        9.8.5 uniq: Example and Code Variations

###        9.8.6 uniq: Why Produce a List?

##      9.9 Monomorphic Lists and Polymorphic Types


#    10 Introduction to Structured Data

##      10.1 Understanding the Kinds of Compound Data

###        10.1.1 A First Peek at Structured Data

###        10.1.2 A First Peek at Conditional Data

##      10.2 Defining and Creating Structured and Conditional Data

###        10.2.1 Defining and Creating Structured Data

###        10.2.2 Annotations for Structured Data

###        10.2.3 Defining and Creating Conditional Data

##      10.3 Programming with Structured and Conditional Data

###        10.3.1 Extracting Fields from Structured Data

###        10.3.2 Telling Apart Variants of Conditional Data

###        10.3.3 Processing Fields of Variants


#    11 Collections of Structured Data

##      11.1 Lists as Collective Data

##      11.2 Sets as Collective Data

###        11.2.1 Picking Elements from Sets

###        11.2.2 Computing with Sets

##      11.3 Combining Structured and Collective Data


#    12 Recursive Data


#    13 Interactive Games as Reactive Systems

##      13.1 About Reactive Animations

##      13.2 Preliminaries

##      13.3 Version: Airplane Moving Across the Screen

###        13.3.1 Updating the World State

###        13.3.2 Displaying the World State

###        13.3.3 Observing Time (and Combining the Pieces)

##      13.4 Version: Wrapping Around

##      13.5 Version: Descending

###        13.5.1 Moving the Airplane

###        13.5.2 Drawing the Scene

###        13.5.3 Finishing Touches

##      13.6 Version: Responding to Keystrokes

##      13.7 Version: Landing

##      13.8 Version: A Fixed Balloon

##      13.9 Version: Keep Your Eye on the Tank

##      13.10 Version: The Balloon Moves, Too

##      13.11 Version: One, Two, ..., Ninety-Nine Luftballons!


#    14 Examples, Testing, and Program Checking

##      14.1 From Examples to Tests

##      14.2 More Refined Comparisons

##      14.3 When Tests Fail

##      14.4 Oracles for Testing

##      14.5 Testing Erroneous Programs


#    15 Functions as Data

##      15.1 A Little Calculus

##      15.2 A Helpful Shorthand for Anonymous Functions

##      15.3 Streams From Functions

##      15.4 Combining Forces: Streams of Derivatives


#    16 Predicting Growth

##      16.1 A Little (True) Story

##      16.2 The Analytical Idea

##      16.3 A Cost Model for Pyret Running Time

##      16.4 The Size of the Input

##      16.5 The Tabular Method for Singly-Structurally-Recursive Functions

##      16.6 Creating Recurrences

##      16.7 A Notation for Functions

##      16.8 Comparing Functions

##      16.9 Combining Big-Oh Without Woe

##      16.10 Solving Recurrences


#    17 Sets Appeal

##      17.1 Representing Sets by Lists

###        17.1.1 Representation Choices

###        17.1.2 Time Complexity

###        17.1.3 Choosing Between Representations

###        17.1.4 Other Operations

##      17.2 Making Sets Grow on Trees

###        17.2.1 Converting Values to Ordered Values

###        17.2.2 Using Binary Trees

###        17.2.3 A Fine Balance: Tree Surgery

####          17.2.3.1 Left-Left Case

####          17.2.3.2 Left-Right Case

####          17.2.3.3 Any Other Cases?


#    18 Halloween Analysis

##      18.1 A First Example

##      18.2 The New Form of Analysis

##      18.3 An Example: Queues from Lists

###        18.3.1 List Representations

###        18.3.2 A First Analysis

###        18.3.3 More Liberal Sequences of Operations

###        18.3.4 A Second Analysis

###        18.3.5 Amortization Versus Individual Operations

##      18.4 Reading More


#    19 Sharing and Equality

##      19.1 Re-Examining Equality

##      19.2 The Cost of Evaluating References

##      19.3 On the Internet, Nobody Knows You’re a DAG

##      19.4 From Acyclicity to Cycles


#    20 Graphs

##      20.1 Understanding Graphs

##      20.2 Representations

###        20.2.1 Links by Name

###        20.2.2 Links by Indices

###        20.2.3 A List of Edges

###        20.2.4 Abstracting Representations

##      20.3 Measuring Complexity for Graphs

##      20.4 Reachability

###        20.4.1 Simple Recursion

###        20.4.2 Cleaning up the Loop

###        20.4.3 Traversal with Memory

###        20.4.4 A Better Interface

##      20.5 Depth- and Breadth-First Traversals

##      20.6 Graphs With Weighted Edges

##      20.7 Shortest (or Lightest) Paths

##      20.8 Moravian Spanning Trees

###        20.8.1 The Problem

###        20.8.2 A Greedy Solution

###        20.8.3 Another Greedy Solution

###        20.8.4 A Third Solution

###        20.8.5 Checking Component Connectedness


#    21 State, Change, and More Equality

##      21.1 A Canonical Mutable Structure

##      21.2 Equality and Mutation

###        21.2.1 Observing Mutation

###        21.2.2 What it Means to be Identical

###        21.2.3 An Additional Challenge

##      21.3 Recursion and Cycles from Mutation

###        21.3.1 Partial Definitions

###        21.3.2 Recursive Functions

###        21.3.3 Premature Evaluation

###        21.3.4 Cyclic Lists Versus Streams

##      21.4 From Identifiers to Variables

##      21.5 Interaction of Mutation with Closures: Counters

###        21.5.1 Implementation Using Boxes

###        21.5.2 Implementation Using Variables

##      21.6 A Family of Equality Predicates

###        21.6.1 A Hierarchy of Equality

###        21.6.2 Space and Time Complexity

###        21.6.3 Comparing Functions


#    22 Algorithms That Exploit State

##      22.1 Disjoint Sets Redux

###        22.1.1 Optimizations

###        22.1.2 Analysis

##      22.2 Set Membership by Hashing Redux

###        22.2.1 Improving Access Time

###        22.2.2 Better Hashing

###        22.2.3 Bloom Filters

##      22.3 Avoiding Recomputation by Remembering Answers

###        22.3.1 An Interesting Numeric Sequence

####          22.3.1.1 Using State to Remember Past Answers

####          22.3.1.2 From a Tree of Computation to a DAG

####          22.3.1.3 The Complexity of Numbers

####          22.3.1.4 Abstracting Memoization

###        22.3.2 Edit-Distance for Spelling Correction

###        22.3.3 Nature as a Fat-Fingered Typist

###        22.3.4 Dynamic Programming

####          22.3.4.1 Catalan Numbers with Dynamic Programming

####          22.3.4.2 Levenshtein Distance and Dynamic Programming

###        22.3.5 Contrasting Memoization and Dynamic Programming


#    23 Processing Programs: Parsing

##      23.1 Understanding Languages by Writing Programs About Them

##      23.2 Everything (We Will Say) About Parsing

###        23.2.1 A Lightweight, Built-In First Half of a Parser

###        23.2.2 Completing the Parser

###        23.2.3 Coda


#    24 Processing Programs: A First Look at Interpretation

##      24.1 Representing Arithmetic

##      24.2 Writing an Interpreter

##      24.3 A First Taste of “Semantics”

##      24.4 Desugaring: Growing the Language Without Enlarging It

###        24.4.1 Extension: Binary Subtraction

###        24.4.2 Extension: Unary Negation

##      24.5 A Three-Stage Pipeline


#    25 Interpreting Conditionals

##      25.1 The Design Space of Conditionals

##      25.2 The Game Plan for Conditionals

###        25.2.1 The Interpreter’s Type

###        25.2.2 Updating Arithmetic

###        25.2.3 Defensive Programming

###        25.2.4 Interpreting Conditionals

##      25.3 Growing the Conditional Language


#    26 Interpreting Functions

##      26.1 Adding Functions to the Language

###        26.1.1 Defining Data Representations

###        26.1.2 Growing the Interpreter

###        26.1.3 Substitution

###        26.1.4 The Interpreter, Resumed

###        26.1.5 Oh Wait, There’s More!

##      26.2 From Substitution to Environments

###        26.2.1 Introducing the Environment

###        26.2.2 Interpreting with Environments

###        26.2.3 Deferring Correctly

###        26.2.4 Scope

###        26.2.5 How Bad Is It?

###        26.2.6 The Top-Level Scope

###        26.2.7 Exposing the Environment

##      26.3 Functions Anywhere

###        26.3.1 Functions as Expressions and Values

###        26.3.2 A Small Improvement

###        26.3.3 Nesting Functions

###        26.3.4 Nested Functions and Substitution

###        26.3.5 Updating Values

###        26.3.6 Sugaring Over Anonymity

##      26.4 Recursion and Non-Termination

##      26.5 Functions and Predictability


#    27 Reasoning about Programs: A First Look at Types

##      27.1 Types as a Static Discipline

##      27.2 The Principle of Substitutability

##      27.3 A Type(d) Language and Type Errors

###        27.3.1 Assume-Guarantee Reasoning

##      27.4 A Type Checker for Expressions and Functions

###        27.4.1 A Pure Checker

###        27.4.2 A Calculator and Checker

###        27.4.3 Type-Checking Versus Interpretation

##      27.5 Type-Checking, Testing, and Coverage

##      27.6 Recursion in Code

###        27.6.1 A First Attempt at Typing Recursion

###        27.6.2 Program Termination

###        27.6.3 Typing Recursion

##      27.7 Recursion in Data

###        27.7.1 Recursive Datatype Definitions

###        27.7.2 Introduced Types

###        27.7.3 Selectors

###        27.7.4 Pattern-Matching and Desugaring


#    28 Safety and Soundness

##      28.1 Safety

##      28.2 “Untyped” Languages

##      28.3 The Central Theorem: Type Soundness

##      28.4 Types, Time, and Space

##      28.5 Types Versus Safety


#    29 Parametric Polymorphism

##      29.1 Parameterized Types

##      29.2 Making Parameters Explicit

##      29.3 Rank-1 Polymorphism

##      29.4 Interpreting Rank-1 Polymorphism as Desugaring

##      29.5 Alternate Implementations

##      29.6 Relational Parametricity


#    30 Type Inference

##      30.1 Type Inference as Type Annotation Insertion

##      30.2 Understanding Inference

###        30.2.1 Constraint Generation

###        30.2.2 Constraint Solving Using Unification

##      30.3 Type Checking and Type Errors

##      30.4 Over- and Under-Constrained Solutions

##      30.5 Let-Polymorphism


#    31 Mutation: Structures and Variables

##      31.1 Separating Meaning from Notation

##      31.2 Mutation and Closures

##      31.3 Mutable Structures

###        31.3.1 Extending the Language Representation

###        31.3.2 The Interpretation of Boxes

###        31.3.3 Can the Environment Help?

###        31.3.4 Welcome to the Store

###        31.3.5 Interpreting Boxes

###        31.3.6 Implementing Mutation: Subtleties and Variations

##      31.4 Variables

###        31.4.1 The Syntax of Variable Assignment

###        31.4.2 Interpreting Variables

###        31.4.3 Reference Parameter Passing

##      31.5 The Design of Stateful Language Operations

##      31.6 Typing State

###        31.6.1 Mutation and Polymorphism

###        31.6.2 Typing the Initial Value


#    32 Objects: Interpretation and Types

##      32.1 Interpreting Objects

##      32.2 Objects by Desugaring

###        32.2.1 Objects as Named Collections

###        32.2.2 Constructors

###        32.2.3 State

###        32.2.4 Private Members

###        32.2.5 Static Members

###        32.2.6 Objects with Self-Reference

####          32.2.6.1 Self-Reference Using Mutation

####          32.2.6.2 Self-Reference Without Mutation

###        32.2.7 Dynamic Dispatch

##      32.3 Member Access Design Space

##      32.4 What (Goes In) Else?

###        32.4.1 Classes

###        32.4.2 Prototypes

###        32.4.3 Multiple Inheritance

###        32.4.4 Super-Duper!

###        32.4.5 Mixins and Traits

##      32.5 Object Classification and Object Equality

##      32.6 Types for Objects

###        32.6.1 Subtyping

####          32.6.1.1 Subtyping Functions

####          32.6.1.2 Subtyping and Information Hiding

####          32.6.1.3 Implementing Subtyping

###        32.6.2 Types for Self-Reference

###        32.6.3 Nominal Types


#    33 Control Operations

##      33.1 Control on the Web

###        33.1.1 Program Decomposition into Now and Later

###        33.1.2 A Partial Solution

###        33.1.3 Achieving Statelessness

###        33.1.4 Interaction with State

##      33.2 Conversion to Continuation-Passing Style

###        33.2.1 Implementation by Desugaring

###        33.2.2 Understanding the Output

###        33.2.3 An Interaction Primitive by Transformation

##      33.3 Implementation in the Core

###        33.3.1 Converting the Interpreter

###        33.3.2 An Interaction Primitive in the Core

##      33.4 Generators

##      33.5 Continuations and Stacks

##      33.6 Tail Calls


#    34 Pyret for Racketeers and Schemers

##      34.1 Numbers, Strings, and Booleans

##      34.2 Infix Expressions

##      34.3 Function Definition and Application

##      34.4 Tests

##      34.5 Variable Names

##      34.6 Data Definitions

##      34.7 Conditionals

##      34.8 Lists

##      34.9 First-Class Functions

##      34.10 Annotations

##      34.11 What Else?


#    35 Glossary
