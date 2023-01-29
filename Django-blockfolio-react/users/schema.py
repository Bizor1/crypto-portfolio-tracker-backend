from urllib import request
import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from django.contrib.auth.models import User
from .models import ExtendUser
from .models import Transactions
from datetime import datetime
from graphene import InputObjectType, String, Int
from graphene import ObjectType, String, Schema

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   update_account = mutations.UpdateAccount.Field()
   resend_activation_email = mutations.ResendActivationEmail.Field()
   send_password_reset_email = mutations.SendPasswordResetEmail.Field()
   password_reset = mutations.PasswordReset.Field()
   password_change = mutations.PasswordChange.Field()
   refresh_token = mutations.RefreshToken.Field()
#    token_auth = mutations.ObtainJSONWebToken.Field()
#    verify_token = mutations.VerifyToken.Field()
#    refresh_token = mutations.RefreshToken.Field()
#    revoke_token = mutations.RevokeToken.Field()

class UserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields = ("id", "email")

class TransactionType(DjangoObjectType):
    class Meta:
        model=Transactions
        fields=('id','date_created','asset','amount','price','transaction_type','user')
    
# class TransactionInput(graphene.InputObjectType):
#     asset = String(required=True)
#     amount = Int(required=True)
#     price = Int(required=True)
#     transactionType = String(required=True)
    # note = String(required=False)

class CreateTransaction(graphene.Mutation):
    class Arguments:
        # amount = graphene.InputField(type=int,required=True)
        # date_created=graphene.String(required=True)
        # amount=graphene.InputField(type=int ,required=True)
        # price=graphene.InputField(type=int,required=True)
        # asset=graphene.InputField(type=str, required=True)
        # transaction_type=graphene.InputField(type=str,required=True)
        amount = graphene.Float()
        print(amount)
        price = graphene.Float()
        transaction_type = graphene.String()
        print('yes')
        asset = graphene.String()
        user=graphene.String()
        print(amount,asset,price,transaction_type)
        # transaction = TransactionInput(required=True)


    transaction = graphene.Field(lambda: TransactionType)

    def mutate(self, info, amount,asset,price,transaction_type,user):
        print("creating")
        username=ExtendUser.objects.get(username=user)
        print(username)
        date_created=datetime.now()
        print(date_created)
        print('still creating')
        
        # user = graphene.Node.get_node_from_global_id(info, user_id, only_type=UserType)
        transaction = Transactions.objects.create(user=username, amount=amount,date_created=date_created,asset=asset,price=price,transaction_type=transaction_type)
        return CreateTransaction(transaction=transaction)
       
            
class Query(UserQuery, MeQuery, graphene.ObjectType):
    # all_transactions = graphene.List(TransactionType)
    specific_user=graphene.Field(UserType,username=graphene.String())
    specific_transaction=graphene.List(TransactionType,username=graphene.String())


    # def resolve_all_transactions(root, info):
    #     return Transactions.objects.all()

    def resolve_specific_transaction(root,info,username,**kwargs):
        
        print("yesdfsdfasgsgfsgfdbd")
        transactions_list=[]
        user_id=ExtendUser.objects.get(username=username)
        id=user_id.id
        transactions=Transactions.objects.filter(user=id)
        for i in transactions:
            transactions_list.append(i)
            print("hjdgjhdshhjsd",i)
        
        # transactions_list.append(transactions)
        print(transactions)
        return transactions_list

    def resolve_specific_user(root,info,username):
        return ExtendUser.objects.get(username=username)
    # pass
    # all_list=graphene.List(TransactionType)

    # def resolve_all_transactions(root, info):
    #     return Transactions.objects.all()

  

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (first_name) for the Field and returns data for the query Response
    # hello = String(name=String(default_value="stranger"))
    # goodbye = String()

    # # our Resolver method takes the GraphQL context (root, info) as well as
    # # Argument (name) for the Field and returns data for the query Response
    # def resolve_hello(root, info, name):
    #     return f'Hello {name}!'

    # def resolve_goodbye(root, info):
    #     return 'See ya!'
    # def resolve_all_users(root, info):
    #     print(info.context.user.id)
    #     print(type("dsd"))


    #     return ExtendUser.objects.all()


class Mutation(AuthMutation, graphene.ObjectType):
    print('dsds')
    # pass
#    class Mutation(graphene.ObjectType):
    # print('creating transaction')
    create_transaction = CreateTransaction.Field()

    # def resolve_my_string(self, info):
    #     return "Hello World"







# class TransactionMutation(graphene.Mutation):

#     class Arguments:
#         date_created=graphene.string(required=True)
#         asset=graphene.DateTime()
#         amount=graphene.Float(required=True)
#         price=graphene.Float(required=True)
#         transaction_type=graphene.String(required=True)
#         user=graphene.









# class Query(graphene.ObjectType):

#     all_users = graphene.List(UserType)
    # all_transactions=graphene.List(TransactionType)

#     all_quizes=graphene.Field(QuizzesType,id=graphene.Int())
#     all_questions=graphene.Field(QuestionType,id=graphene.Int())
#     all_answers=graphene.List(AnswerType,id=graphene.Int())

    
#     quiz=graphene.String()

    # def resolve_all_users(root, info):
    #     print(info.context.user.id)
    #     print(type("dsd"))


    #     return ExtendUser.objects.all()
        
    # def resolve_all_transactions(root, info):
    #     return Transactions.objects.all()

    
#     def resolve_all_quizes(root,info,id):
#         return Quizzes.objects.get(pk=id)

#     def resolve_all_questions(root,info,id):
#         return Question.objects.get(pk=id) 

#     def resolve_all_answers(root,info,id):
#         return Answer.objects.filter(question=id)
# class CurrentUserType(DjangoObjectType):
#     class Meta:
#         model = User
#         fields = ("id",)




schema = graphene.Schema(query=Query, mutation=Mutation)