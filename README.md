# GoShop Field Service Enhancement

## Rationale

The proposed enhancements aim to optimize GoShop's service delivery and project management processes. By incorporating "Service Location" data into the contact form and sales orders, the system facilitates efficient tracking and resource allocation for services such as solar installations or genset maintenance. These improvements align with our goal to scale operations and enhance the promotion of services.

The mandatory "Services Instructions" field ensures clear and consistent communication of relevant task details, reducing potential errors or misunderstandings. Consolidating instructions for multiple services into a single field on the Sales Order (SO) simplifies project management and improves clarity. The same applies to the material lists displayed on the task.

## Specification

### 1. Contact Form Modification

- Add a new address type: "Service Location"
- Include a star button to display the count of "Service Locations" associated with each company or individual.
- Fields for "Service Location" info:
  - Contact Name
  - Phone
  - Email
  - Equipment Name
  - Address (Street, City, Country)
  - Type: Select (Solar, Water Heater, Genset, Air Conditioning, Other)
  - If "Other" is selected, provide a text field to input details.
  - Internal Notes

### 2. Sales Order (SO) Updates

- Integrate the "Service Location" field below the other address fields.
- Add a "Services Instructions" tab:
  - This tab is visible only if a service product creating a task is added to the SO.
  - Field is an HTML one.
  - Make the "Service Instructions" mandatory.

### 3. Task Generation and Management

- On task generation upon SO validation, add a tag by default with the name of the Warehouse linked to the Sale Order.
- Duplicate the content from "Services Instructions" into the task's description.
- Below the instructions, include a table listing materials (product name, product description, and quantity ordered).
- Add a "Service Location" field on the task (below other address fields).
- Add a star button linked to the deliveries and display delivery status on the task.
- Display the task ID as a read-only field.
- On the report, display the task ID.

## Getting Started

To test the new features, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/GoShop-Energy/field-service.git
   ```
