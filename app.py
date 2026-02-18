import streamlit as st
import json
import os

FILE_NAME = "tasks.json"


# ----------------------------
# Load tasks
# ----------------------------
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


# ----------------------------
# Save tasks
# ----------------------------
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


# ----------------------------
# Initialize tasks
# ----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()


st.title("📝 To-Do List App")

# ----------------------------
# Add Task
# ----------------------------
st.subheader("Add New Task")

new_task = st.text_input("Enter Task")

if st.button("Add Task"):
    if new_task.strip() != "":
        st.session_state.tasks.append(
            {"title": new_task, "completed": False}
        )
        save_tasks(st.session_state.tasks)
        st.success("Task Added Successfully!")
    else:
        st.warning("Task cannot be empty")


# ----------------------------
# Show All Tasks
# ----------------------------
st.subheader("All Tasks")

if st.session_state.tasks:
    for index, task in enumerate(st.session_state.tasks):

        col1, col2, col3 = st.columns([6, 2, 2])

        with col1:
            if task["completed"]:
                st.markdown(f"~~{task['title']}~~ ✅")
            else:
                st.write(task["title"])

        with col2:
            if not task["completed"]:
                if st.button("Complete", key=f"complete{index}"):
                    st.session_state.tasks[index]["completed"] = True
                    save_tasks(st.session_state.tasks)
                    st.rerun()

        with col3:
            if st.button("Delete", key=f"delete{index}"):
                st.session_state.tasks.pop(index)
                save_tasks(st.session_state.tasks)
                st.rerun()
else:
    st.info("No tasks added yet.")


# ----------------------------
# Show Pending Tasks
# ----------------------------
st.subheader("Pending Tasks")

pending_tasks = [
    task for task in st.session_state.tasks
    if not task["completed"]
]

if pending_tasks:
    for task in pending_tasks:
        st.write(task["title"])
else:
    st.success("No Pending Tasks 🎉")
