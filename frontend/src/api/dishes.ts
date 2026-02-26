import { api } from "./client";

export type Dish = {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
};

export type CreateDishPayload = {
  name: string;
  description?: string;
};

export type UpdateDishPayload = {
  name?: string;
  description?: string;
};

export async function listDishes() {
  const response = await api.get<Dish[]>("/dishes");
  return response.data;
}

export async function createDish(payload: CreateDishPayload) {
  const response = await api.post<Dish>("/dishes", payload);
  return response.data;
}

export async function updateDish(dishId: number, payload: UpdateDishPayload) {
  const response = await api.put<Dish>(`/dishes/${dishId}`, payload);
  return response.data;
}

export async function deleteDish(dishId: number) {
  await api.delete(`/dishes/${dishId}`);
}
