import resource

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from .models import (Settlement, Transaction, RecentTransaction,
                     Category, Budgets, Comment)
from datetime import date
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from actions.models import Activity



# Create your views here.


def finance_list(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.username == 'user' and user.is_active:
                # Regular user
                login(request, user)
                request.session['user_role'] = 'user'  # Store user role in session
                request.session['display_name'] = 'Ankit'  # Store display name in session
                return redirect('finance:dashboard')  # Redirect to the user dashboard
            elif user.username == 'admin' and user.is_active:
                # Admin user
                login(request, user)
                request.session['user_role'] = 'admin'  # Store user role in session
                request.session['display_name'] = 'Admin User'  # Store display name in session
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
        else:
            # Invalid login
            return render(request, "finance/finance_story/../templates/user/login.html",
                          {'error_message': 'Invalid login credentials'})

    return render(request, "finance/finance_story/../templates/user/login.html")


def activity_feed(request):
    # Get the recent actions
    actions = Activity.objects.all().order_by('-created')[:10]
    return render(request, 'finance/baseHome.html', {'actions': actions})


def dashboard(request):
    settlements = Settlement.objects.all()
    actions = Activity.objects.all().order_by('-created')[:10]
    recentTransactions = RecentTransaction.objects.all().filter(flag=0)
    upcomingPayments = RecentTransaction.objects.all().filter(flag=1)
    context = {"settlements": settlements,
               "recentTransactions": recentTransactions,
               "upcomingPayments": upcomingPayments,
               "actions": actions}
    return render(request,
                  "finance/finance_story/dashboard.html",
                  context
                  )


def transaction(request):
    actions = Activity.objects.all().order_by('-created')[:10]
    transactions = Transaction.objects.order_by('-date')  # Ordering transactions by 'transaction_number'
    context = {
        "transactions": transactions,
        "actions": actions,
    }
    user = User.objects.get(username=request.session.get("username"))
    if request.method == 'POST':
        # process the add transaction form
        purpose = request.POST.get('purpose')
        amount = float(request.POST.get('amount'))
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        new_transaction = Transaction(purpose=purpose, categoryField=category, amount=amount)
        new_transaction.save()
        transactions = Transaction.objects.order_by('-date')
        context['transactions'] = transactions

        action = Activity(
            user=user,
            verb="created transaction",
            target=new_transaction
        )
        action.save()
        messages.success(request, 'New transaction added successfully.')

    return render(request,
                  "finance/finance_story/transactions.html",
                  context
                  )


def totalBudget(request):
    actions = Activity.objects.all().order_by('-created')[:10]
    budgets = Budgets.objects.all()
    categories = Category.objects.all()
    context = {"categories": categories,
               "budgets": budgets,
               "actions": actions,
               }
    user = User.objects.get(username=request.session.get("username"))
    if request.method == 'POST':
        # Get all the amount fields from the form
        amounts = request.POST.getlist('amount')
        total_amount = 0  # Initialize the total amount
        for amount in amounts:
            if amount:  # Check if the amount is not an empty string
                total_amount += float(amount)  # add the amounts

        today = date.today()
        budget, created = Budgets.objects.get_or_create(date=today)
        budget.amount = f"${total_amount:.2f}"  # Format the total_amount with a dollar sign
        budget.save()

        messages.success(request, 'New Budget created successfully.')
    return render(request,
                  "finance/finance_story/totalBudget.html",
                  context
                  )


def searchResults(request):
    return render(request, "finance/finance_story/search-results.html")


def search_transactions(request):
    if request.method == 'GET' and 'query' in request.GET:
        search_query = request.GET.get('query')

        transactions = Transaction.objects.filter(purpose__icontains=search_query)
        transaction_list = []
        for transaction in transactions:
            # Get the related category name
            category_name = transaction.categoryField.name  # the categoryField is a ForeignKey to the Category table

            transaction_dict = {
                'transaction_number': transaction.transaction_number,
                'purpose': transaction.purpose,
                'category': category_name,  # Include the category name in the response
                'date': transaction.date,
                'amount': transaction.amount
            }
            transaction_list.append(transaction_dict)

        data = {'transactions': transaction_list}

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request'})


def updateDeleteTransaciton(request):
    transactions = Transaction.objects.order_by('-date')  # Ordering transactions by 'transaction_number'
    actions = Activity.objects.all().order_by('-created')[:10]
    context = {
        "transactions": transactions,
        "actions": actions
    }
    if request.method == 'POST':
        # Get the transaction number from the header
        transaction_number = request.POST.get('transaction_number')

        if 'save' in request.POST:  # Check if Save button is clicked
            # Get the updated fields from the form
            purpose = request.POST.get('purpose')
            category_name = request.POST.get('category')
            # Search for the category in the database
            category = Category.objects.get(name=category_name)
            if category:
                category_id = category.id
            amount = float(request.POST.get('amount'))
            date = request.POST.get('date')
            # Get the specific transaction object
            transaction = Transaction.objects.get(transaction_number=transaction_number)
            # Update the transaction fields
            transaction.purpose = purpose
            transaction.categoryField = category
            transaction.amount = amount
            transaction.date = date
            transaction.save()
            messages.success(request, 'Transaction updated successfully.')
        elif 'delete' in request.POST:  # Check if Delete button is clicked
            # Get the specific transaction object and delete it
            transaction = Transaction.objects.get(transaction_number=transaction_number)
            transaction.delete()
            messages.success(request, 'Transaction deleted successfully.')

    return render(request, "finance/finance_story/transactions.html", context)


def updateTransaction(request, transaction_number):
    target_transaction = None
    actions = Activity.objects.all().order_by('-created')[:10]
    transactions = Transaction.objects.all()
    for transaction in transactions:
        if transaction.transaction_number == transaction_number:
            target_transaction = transaction
            break

    if target_transaction:
        return render(request, 'finance/finance_story/detail.html', {'transaction': target_transaction, 'actions': actions})


def settlement_detail(request, settlement_id):
    actions = Activity.objects.all().order_by('-created')[:10]
    # Fetch the specific settlement by ID
    settlement = get_object_or_404(Settlement, pk=settlement_id)

    # Fetch comments related to the settlement, ordered by creation date (newest first)
    comments = Comment.objects.filter(settlement=settlement).order_by('-created_at')

    # Render the template with the settlement and its comments
    return render(request, 'finance/finance_story/settlement_detail.html', {
        'settlement': settlement,
        'comments': comments,
        "actions": actions,
    })


def post_comment(request, settlement_id):
    if request.method == "POST" and request.user.is_authenticated:
        settlement = get_object_or_404(Settlement, pk=settlement_id)
        comment_text = request.POST.get('text')
        Comment.objects.create(settlement=settlement, user=request.user, text=comment_text)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    settlement_id = comment.settlement.id  # Assuming a foreign key to Settlement
    actions = Activity.objects.all().order_by('-created')[:10]
    if not request.user.is_superuser and request.user != comment.user:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('finance:settlement_detail', settlement_id=settlement_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('finance:settlement_detail', settlement_id=settlement_id)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CommentForm(instance=comment)

    return render(request, 'finance/finance_story/edit_comment.html', {'form': form, 'comment': comment, 'actions':actions,})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    settlement_id = comment.settlement.id  # Assuming a foreign key to Settlement

    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect('finance:settlement_detail', settlement_id=settlement_id)
