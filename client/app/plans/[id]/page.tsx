import { notFound } from 'next/navigation';
import { readPlan } from '@/app/lib/actions';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const id = params.id;
  const plan = await readPlan(id);

  if (!plan) {
    notFound();
  }

  return (
    <div>
      <p>{plan.title}</p>
      <p>{plan.description}</p>
    </div>
  );
}
