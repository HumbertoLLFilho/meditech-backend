from dataclasses import dataclass


@dataclass
class ListarUsuariosInput:
    ativo: bool | None = None
    tipo: str | None = None
    nome: str | None = None
    cpf: str | None = None
    ordem: str = "desc"

    @staticmethod
    def from_args(args: dict) -> "ListarUsuariosInput":
        ativo = None
        if "ativo" in args:
            valor = args["ativo"].lower()
            if valor not in ("true", "false"):
                raise ValueError("Filtro 'ativo' deve ser 'true' ou 'false'.")
            ativo = valor == "true"

        ordem = args.get("ordem", "desc").lower()
        if ordem not in ("asc", "desc"):
            raise ValueError("Parametro 'ordem' deve ser 'asc' ou 'desc'.")

        return ListarUsuariosInput(
            ativo=ativo,
            tipo=args.get("tipo") or None,
            nome=args.get("nome") or None,
            cpf=args.get("cpf") or None,
            ordem=ordem,
        )
