import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { createDish, deleteDish, listDishes, updateDish } from "../api/dishes";

const dishSchema = z.object({
  name: z.string().min(1, "菜名不能为空").max(255, "菜名最长 255"),
  description: z.string().max(1000, "描述最长 1000 字符").optional(),
});

type DishFormData = z.infer<typeof dishSchema>;

export function DishesPage() {
  const queryClient = useQueryClient();
  const dishesQuery = useQuery({
    queryKey: ["dishes"],
    queryFn: listDishes,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<DishFormData>({
    resolver: zodResolver(dishSchema),
    defaultValues: {
      name: "",
      description: "",
    },
  });

  const createMutation = useMutation({
    mutationFn: createDish,
    onSuccess: async () => {
      reset();
      await queryClient.invalidateQueries({ queryKey: ["dishes"] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ dishId, data }: { dishId: number; data: DishFormData }) => updateDish(dishId, data),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["dishes"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDish,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["dishes"] });
    },
  });

  const onSubmit = (data: DishFormData) => {
    createMutation.mutate(data);
  };

  return (
    <div className="space-y-6">
      <section className="panel">
        <div className="panel-head">
          <h2 className="panel-title">新增菜品</h2>
          <p className="panel-subtitle">支持名称去重，创建后会立即刷新列表。</p>
        </div>

        <form className="space-y-3" onSubmit={handleSubmit(onSubmit)}>
          <div>
            <input className="field-input" placeholder="菜品名称" {...register("name")} />
            {errors.name ? <p className="field-error">{errors.name.message}</p> : null}
          </div>

          <div>
            <textarea className="field-input" placeholder="描述（可选）" rows={3} {...register("description")} />
            {errors.description ? <p className="field-error">{errors.description.message}</p> : null}
          </div>

          <div className="flex items-center gap-3">
            <button className="btn-primary" disabled={createMutation.isPending} type="submit">
              {createMutation.isPending ? "提交中..." : "创建菜品"}
            </button>
            {createMutation.isError ? <p className="form-error">创建失败，请检查是否重名</p> : null}
            {createMutation.isSuccess ? <p className="form-success">创建成功</p> : null}
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-head">
          <h2 className="panel-title">菜品列表</h2>
          <p className="panel-subtitle">可直接在列表中编辑名称和描述，也可删除。</p>
        </div>

        {dishesQuery.isLoading ? <p>加载中...</p> : null}
        {dishesQuery.isError ? <p className="form-error">加载失败，请刷新重试</p> : null}
        {dishesQuery.data && dishesQuery.data.length === 0 ? <p className="text-slate-600">暂无菜品，先创建一个吧。</p> : null}

        <ul className="space-y-3">
          {dishesQuery.data?.map((dish) => (
            <DishItem
              key={dish.id}
              dish={dish}
              isUpdating={updateMutation.isPending}
              isDeleting={deleteMutation.isPending}
              onUpdate={(data) => updateMutation.mutate({ dishId: dish.id, data })}
              onDelete={() => deleteMutation.mutate(dish.id)}
            />
          ))}
        </ul>
      </section>
    </div>
  );
}

function DishItem({
  dish,
  onUpdate,
  onDelete,
  isUpdating,
  isDeleting,
}: {
  dish: { id: number; name: string; description: string | null };
  onUpdate: (data: DishFormData) => void;
  onDelete: () => void;
  isUpdating: boolean;
  isDeleting: boolean;
}) {
  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<DishFormData>({
    resolver: zodResolver(dishSchema),
    defaultValues: {
      name: dish.name,
      description: dish.description ?? "",
    },
  });

  return (
    <li className="dish-card">
      <form className="space-y-2" onSubmit={handleSubmit(onUpdate)}>
        <input className="field-input" {...register("name")} />
        {errors.name ? <p className="field-error">{errors.name.message}</p> : null}

        <textarea className="field-input" rows={2} {...register("description")} />
        {errors.description ? <p className="field-error">{errors.description.message}</p> : null}

        <div className="dish-actions">
          <button className="btn-primary" disabled={!isDirty || isUpdating} type="submit">
            {isUpdating ? "保存中..." : "保存"}
          </button>
          <button className="btn-danger" disabled={isDeleting} onClick={onDelete} type="button">
            {isDeleting ? "删除中..." : "删除"}
          </button>
        </div>
      </form>
    </li>
  );
}
