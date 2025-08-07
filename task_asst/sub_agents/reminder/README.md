# Reminder Agent

Handles all reminder-related tasks for the Task Assistant project.

## Features

- Set reminders with a message and time (natural language supported)
- List all reminders with their status (Done/Pending)
- Delete reminders by index
- Mark reminders as done
- Notifies you on your laptop when a reminder is due (using system notifications)

## Usage Examples

- **Set a reminder:**  
  `"Remind me to call mom at 5pm"`
- **List reminders:**  
  `"Show my reminders"`
- **Delete a reminder:**  
  `"Delete the second reminder"`
- **Mark a reminder as done:**  
  `"Mark the first reminder as done"`

## Implementation Notes

- Reminders are stored in-memory for demonstration purposes.
- Notifications are sent using the `plyer` library.
- Reminder times are parsed using natural language (e.g., "in 10 minutes", "tomorrow at 8am").
- After each operation, control is delegated back to the root agent for further assistance.

---