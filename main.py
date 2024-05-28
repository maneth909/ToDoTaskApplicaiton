import streamlit as st

# Define a Node class for the linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Define a LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task):
        new_node = Node(task)
        # Add task to the last line
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    # Remove using specified index
    def remove_task(self, index):
        task_index = 0
        current = self.head
        previous = None
        removed_task = None

        # Ensure there is something in the list when removing
        while current is not None:
            if task_index == index:
                removed_task = current.data
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                break
            previous = current
            current = current.next
            task_index += 1

        return removed_task

    def display_tasks(self):
        tasks = []
        current = self.head

        while current is not None:
            tasks.append(current.data)
            current = current.next

        return tasks

# Initialize the linked list in session state if not already initialized
if 'all_tasks' not in st.session_state:
    st.session_state.all_tasks = LinkedList()

if 'removal' not in st.session_state:
    st.session_state.removal = None

# Create a Streamlit app
def main():
    st.title("To-Do List App with Linked List")

    # Sidebar for adding tasks
    task_input = st.sidebar.text_input("Add Task", key="add_task_input")
    if st.sidebar.button("Add Task", key="add_task_button"):
        if task_input:
            st.session_state.all_tasks.add_task(task_input)
            st.experimental_rerun()  # Rerun to clear the input box

    # Sidebar for removing tasks by index
    remove_index = st.sidebar.number_input("Remove Task by Index", min_value=1, step=1, key="remove_task_input")
    if st.sidebar.button("Remove Task", key="remove_task_button"):
        removed_task = st.session_state.all_tasks.remove_task(remove_index - 1)
        if removed_task:
            st.session_state.removal = removed_task
        st.experimental_rerun() 

    # Display last removed task in red
    if st.session_state.removal:
        st.sidebar.markdown(f"<p style='color: red;'>Last removed task: {st.session_state.removal}</p>", unsafe_allow_html=True)

    # Undo the last removal
    if st.sidebar.button("Undo", key="undo_remove_button"):
        if st.session_state.removal:
            st.session_state.all_tasks.add_task(st.session_state.removal)
            st.session_state.removal = None
        st.experimental_rerun() 

    # Main content to display tasks
    st.write("## Your To-Do List:")
    tasks = st.session_state.all_tasks.display_tasks()

    if not tasks:
        st.write("No tasks yet. Add some tasks using the sidebar!")

    for i, task in enumerate(tasks, start=1):
        st.write(f"{i}. {task}")

if __name__ == "__main__":
    main()
