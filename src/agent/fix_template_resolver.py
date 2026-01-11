from agent.fix_template import FixTemplate
from rules.issue import Issue


class FixTemplateResolver:
    """
    Maps detected issues to fix templates
    """

    def resolve(self, issue: Issue) -> FixTemplate:

        if issue.name == "Static Cache Leak":
            return self._static_cache_fix(issue)
        if issue.name == "ThreadLocal Memory Leak":
            return self._threadLocal_fix(issue)
        if issue.name == "ClassLoader Memory Leak":
            return self._classloader_fix(issue)

        return  self._generic_fix(issue)

    # ------------------------
    # Static cache leak
    # ------------------------

    def _static_cache_fix(self, issue) -> FixTemplate:
        return FixTemplate(
            title="Fix Static Cache Memory Leak",
            summary= (
                "A static cache is retaining memory for the entire JVM lifetime. "
                "Without eviction or lifecycle management, memory will grow unbounded"
            ),

            actions=[
                "Introduce size-based or time-based eviction (LRU/TTL)",
                "Avoid static caches until absolutely necessary",
                "Clear the cache during application shutdown",
                "Consider using a mature cache library(Caffeine, Guava)"
            ],
            risks_if_ignored=(
                "Heap usage will continue to grow, eventually causing "
                "OutOfMemoryError and JVM restarts"
            )

        )

    # ------------------------
    # ThreadLocal leak
    # ------------------------

    def _threadLocal_fix(self, issue) -> FixTemplate:
        return FixTemplate(
            title="Fix ThreadLocal Memory Leak",
            summary=(
                "Objects stored in ThreadLocal variables are retained for lifetime "
                "of the thread. In thread pools, this can cause long -lived memory leaks."
            ),
            actions=[
                "Always call ThreadLocal.remove() ina finally block.",
                "Avoid storing large objects in ThreadLocal.",
                "Ensure ThreadLocal usage is scoped to request lifecycle.",
                "Audit frameworks or libraries using ThreadLocal internally"
            ],
            risks_if_ignored=(
                "Memory retained by thread pools will accumulate and may cause"
                "OutOfMemoryError under sustained load"
            )

        )

    # ------------------------
    # ClassLoader leak
    # ------------------------

    def _classloader_fix(self, issue) -> FixTemplate:
        return FixTemplate(
            title="Fix ClassLoader Memory Leak",
            summary=(
                "Classes from an old ClassLoader are still reachable, preventing"
                "garbage collection during application redeployments."
            ),
            actions=[
                "Ensure all static references are cleared on application shutdown.",
                "Stop background threads started by the application",
                "Avoid caching application classes in global singletons.",
                "Verify listeners, executors, and thread pools are properly shut down."
            ],
            risks_if_ignored=(
                "Each redeployment will leak memory, eventually exhausting heap"
                "or metaspace and forcing JVM restarts."
            )
        )

    # ------------------------
    # Generic fallback
    # ------------------------
    def _generic_fix(self, issue) -> FixTemplate:
        return FixTemplate(
            title="Investigate Memory Retention",
            summary="Significant memory retention was detected.",
            actions=[
                "Analyze GC root paths to identify ownership.",
                "Review object lifecycle and reference management.",
                "Add monitoring to track memory growth over time."
            ],
            risks_if_ignored="Potential memory pressure and instability"
        )


