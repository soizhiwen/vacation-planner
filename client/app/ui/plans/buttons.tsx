import Form from 'next/form';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';
import { deletePlan } from '@/app/lib/actions';

export function CreatePlan({ isPending }: { isPending: boolean }) {
    return (
        <button
            type="submit"
            disabled={isPending}
            className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
            <span className="hidden md:block">Create Plan</span>{' '}
            <PlusIcon className="h-5 md:ml-4" />
        </button>
    );
}


export function DeletePlan({ id }: { id: string }) {
    const deletePlanWithId = deletePlan.bind(null, id);

    return (
        <Form action={deletePlanWithId}>
            <button
                type="submit"
                className="rounded-md border p-2 hover:bg-gray-100"
            >
                <span className="sr-only">Delete</span>
                <TrashIcon className="w-5" />
            </button>
        </Form>
    );
}
