import { memberAdded } from '../showcase';

export default function registerMemberAddedEvents() {
  memberAdded(async (data) => {
    console.log(data.memberAdded.project.name, data.memberAdded.username);
  });
}
