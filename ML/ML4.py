
# Gradient Descent Algorithm to Find Local Minimum

import matplotlib.pyplot as plt

# 1. Define the function
def f(x):
    return x ** 2

# 2. Define the derivative
def derivative(x):
    return 2 * x

# 3. Initialize parameters
x = 10
learning_rate = 0.1
iterations = 100

# Store values for visualization
x_history = []

# 4. Gradient Descent Algorithm
for i in range(iterations):

    x_history.append(x)

    # Calculate gradient
    grad = derivative(x)

    # Update x
    x = x - learning_rate * grad

# 5. Display Result
print("Minimum value of x:", x)
print("Minimum value of function:", f(x))

# 6. Plot the function
x_values = [i / 10 for i in range(-100, 101)]
y_values = [f(i) for i in x_values]

plt.plot(x_values, y_values, label="f(x) = x^2")

# Plot Gradient Descent steps
plt.scatter(
    x_history,
    [f(i) for i in x_history],
    color="red",
    label="Gradient Descent"
)

plt.title("Gradient Descent Optimization")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
plt.show()
