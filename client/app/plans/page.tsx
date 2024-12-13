import { notFound } from 'next/navigation';
import { readPlans } from '@/app/lib/actions';

export default async function Page(props: {
  searchParams?: Promise<{
    limit?: string;
  }>;
}) {
  const searchParams = await props.searchParams;
  const limit = Number(searchParams?.limit) || 10;
  const plans = await readPlans(limit);

  if (!plans) {
    notFound();
  }

  return (
    <div>
      {plans &&
        plans.map((plan: any) => (
          <div key={plan._id}>
            <p>
              {plan.title}
            </p>
            <p>
              {plan.description}
            </p>
          </div>
        ))}
    </div>
  );
}
