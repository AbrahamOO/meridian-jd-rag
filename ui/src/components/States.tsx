interface MessageProps {
  title: string;
  detail?: string;
}

export function Loading({ title = "Loading", detail }: Partial<MessageProps>) {
  return (
    <div className="state" role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <div>{title}</div>
      {detail ? <div className="small muted">{detail}</div> : null}
    </div>
  );
}

export function ErrorState({ title, detail }: MessageProps) {
  return (
    <div className="state error" role="alert">
      <strong>{title}</strong>
      {detail ? <div className="small">{detail}</div> : null}
    </div>
  );
}

export function EmptyState({ title, detail }: MessageProps) {
  return (
    <div className="state">
      <strong>{title}</strong>
      {detail ? <div className="small muted">{detail}</div> : null}
    </div>
  );
}
