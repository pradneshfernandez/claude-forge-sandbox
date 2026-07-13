import argparse
import sys

import core
import storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("text", type=str)

    subparsers.add_parser("list")

    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)

    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("id", type=int)

    return parser


def main(argv: list | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    path = storage.resolve_path()
    try:
        todos = storage.load(path)
    except storage.CorruptStoreError as e:
        print(f"error: corrupt store: {e}", file=sys.stderr)
        return 2

    if args.cmd == "add":
        try:
            todos, new_id = core.add_todo(todos, args.text)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        storage.save(path, todos)
        print(new_id)
        return 0

    if args.cmd == "list":
        out = core.format_list(todos)
        if out:
            print(out)
        return 0

    if args.cmd == "done":
        try:
            core.mark_done(todos, args.id)
        except KeyError:
            print(f"error: no todo with id {args.id}", file=sys.stderr)
            return 1
        storage.save(path, todos)
        return 0

    if args.cmd == "rm":
        try:
            core.remove_todo(todos, args.id)
        except KeyError:
            print(f"error: no todo with id {args.id}", file=sys.stderr)
            return 1
        storage.save(path, todos)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
