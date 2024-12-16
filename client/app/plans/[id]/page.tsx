import { notFound } from 'next/navigation';
import { readPlan } from '@/app/lib/actions';
import { DeletePlan } from '@/app/ui/plans/buttons';
import { Plan, Day, Activity } from '@/app/lib/definitions';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const id = params.id;
  const plan: Plan = await readPlan(id);

  if (!plan) {
    notFound();
  }

  let timestamp = new Date(plan.timestamp)

  return (
    <div>
      <p>{plan.title}</p>
      <p>{plan.description}</p>
      <p>{plan.budget}</p>
      <p>{plan.totalDays}</p>
      {plan.days &&
        plan.days.map((day: Day) => (
          <div key={day.day}>
            <p>
              {day.day}
            </p>
            {day.activities &&
              day.activities.map((activity: Activity) => (
                <div key={activity.activity}>
                  <div>
                    <p>
                      {activity.time}
                    </p>
                    <p>
                      {activity.place}
                    </p>
                    <p>
                      {activity.activity}
                    </p>
                    <p>
                      {activity.notes}
                    </p>
                  </div>
                </div >
              ))
            }
          </div >
        ))
      }
      <p>Last update: {timestamp.toLocaleString()}</p>
      <DeletePlan
        id={plan._id}
        isRedirect={true}
      />
    </div>
  );
}
