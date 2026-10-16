import { ChevronDown, ChevronUp, ExternalLink, Sparkles } from "lucide-react";
import Image from "next/image";
import { useMemo, useState } from "react";

import type { Claim } from "@/lib/store";
import { cn, extractDomain } from "@/lib/utils";
import type { ClaimSource } from "@/types";
import { Favicon } from "./ui/favicon";

interface SourcePillsProps {
  verdicts: Claim[];
  maxSources?: number;
}

export const SourcePills = ({ verdicts, maxSources = 8 }: SourcePillsProps) => {
  const [expanded, setExpanded] = useState(false);

  const uniqueSources = useMemo(() => {
    const sources = new Map<string, ClaimSource>();

    for (const verdict of verdicts) {
      for (const source of verdict.sources ?? []) {
        if (!sources.has(source.url)) {
          sources.set(source.url, source);
        } else if (source.is_influential) {
          // If already added but this occurrence is influential, mark it
          const existing = sources.get(source.url)!;
          existing.is_influential = true;
        }
      }
    }

    return Array.from(sources.values());
  }, [verdicts]);

  if (uniqueSources.length === 0) {
    return null;
  }

  // Determine which sources to display
  const displaySources = expanded
    ? uniqueSources
    : uniqueSources.slice(0, maxSources);

  const hasMoreSources = uniqueSources.length > maxSources;
  const hiddenSourcesCount = uniqueSources.length - maxSources;

  return (
    <div className="rounded-xl border border-neutral-200/80 bg-gradient-to-b from-white to-neutral-50/50 p-3.5 shadow-xs">
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <h3 className="font-semibold text-neutral-900 text-sm">Evidence Sources</h3>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-teal-200/80 bg-teal-50/80 px-2 py-0.5 text-[11px] font-medium text-teal-800 shadow-2xs">
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-teal-400 opacity-75" />
              <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-teal-500" />
            </span>
            TinyFish Web Intelligence
          </span>
        </div>

        {hasMoreSources && (
          <button
            className="flex items-center gap-1 rounded-md px-2 py-1 text-neutral-500 text-xs font-medium transition-colors hover:bg-neutral-100 hover:text-neutral-900"
            onClick={() => setExpanded(!expanded)}
            type="button"
          >
            {expanded ? (
              <>
                <span>Show less</span>
                <ChevronUp className="h-3.5 w-3.5" />
              </>
            ) : (
              <>
                <span>Show all {uniqueSources.length}</span>
                <ChevronDown className="h-3.5 w-3.5" />
              </>
            )}
          </button>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {displaySources.map((source) => {
          const domain = extractDomain(source.url);
          const title = source.title || domain;
          const isKeyEvidence = Boolean(source.is_influential);

          return (
            <a
              className={cn(
                "group relative flex items-center gap-2 rounded-lg border px-2.5 py-1 text-xs",
                "bg-white transition-all duration-200 ease-out",
                isKeyEvidence
                  ? "border-teal-300 bg-teal-50/30 text-neutral-800 shadow-2xs hover:border-teal-400 hover:bg-teal-50/70"
                  : "border-neutral-200 text-neutral-700 hover:border-neutral-300 hover:bg-neutral-50 hover:shadow-2xs",
                "focus:outline-none focus:ring-2 focus:ring-teal-500/20"
              )}
              href={source.url}
              key={source.url}
              rel="noreferrer"
              target="_blank"
              title={`${title} (${source.url})`}
            >
              <Favicon url={source.url} />
              <span className="max-w-44 truncate font-medium text-neutral-800 group-hover:text-neutral-900">
                {title}
              </span>
              {isKeyEvidence && (
                <span className="inline-flex items-center gap-0.5 rounded px-1 py-0.2 text-[9px] font-semibold uppercase tracking-wider bg-teal-100 text-teal-800">
                  <Sparkles className="h-2.5 w-2.5 text-teal-600" />
                  Key
                </span>
              )}
              <ExternalLink className="h-3 w-3 flex-shrink-0 text-neutral-400 transition-colors group-hover:text-teal-600" />
            </a>
          );
        })}

        {!expanded && hasMoreSources && (
          <button
            className={cn(
              "flex items-center gap-1 rounded-lg border border-dashed border-neutral-300 bg-neutral-50/80 px-2.5 py-1 text-xs font-medium text-neutral-600",
              "hover:border-neutral-400 hover:bg-neutral-100 hover:text-neutral-900",
              "transition-all duration-150 ease-in-out",
              "focus:outline-none focus:ring-2 focus:ring-teal-500/20"
            )}
            onClick={() => setExpanded(true)}
            type="button"
          >
            +{hiddenSourcesCount} more
            <ChevronDown className="h-3 w-3" />
          </button>
        )}
      </div>
    </div>
  );
};
