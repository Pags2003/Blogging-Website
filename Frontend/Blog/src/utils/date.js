export function formatDate(dateString) {
  if (!dateString) return "Unknown date";
  const d = new Date(dateString);
  return isNaN(d) ? "Invalid date" : d.toLocaleString();
}
