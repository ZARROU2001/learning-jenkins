export interface User {
  id: number; // Assuming the user will have an ID from the backend
  email: string;
  firstName: string;
  lastName: string;
  username: string;
  createdAt?: string; // Optional: Timestamp for when the user was created
  updatedAt?: string; // Optional: Timestamp for the last update
}
