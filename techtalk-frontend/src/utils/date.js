// Format timestamp to human-readable format
import { formatDistanceToNow } from 'date-fns';

export const formatDate = (timestamp) => {
  return formatDistanceToNow(new Date(timestamp), { addSuffix: true });
};