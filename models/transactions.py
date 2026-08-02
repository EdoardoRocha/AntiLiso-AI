from pydantic import BaseModel, Field

# Schema model for transactions collections
class TransacaoSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Valor da transação. Deve ser maior que zero.")
    type: str = Field(..., description="Tipo da transação", pattern="^(gasto|ganho)$")
    category: str = Field(..., description="Categoria da transação (ex: 99moto, comida, salário)")
    description: str = Field(..., description="Breve descrição da transação")
    date: str = Field(..., description="Data da transação no formato DD/MM/YYYY")
