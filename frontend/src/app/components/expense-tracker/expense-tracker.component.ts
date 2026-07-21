import { Component, signal, computed, inject, OnInit } from '@angular/core'; 
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LedgerService, TrackerItem, TrackerType } from '../../services/ledger.service'; 

@Component({
  selector: 'app-expense-tracker',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './expense-tracker.component.html',
})
export class ExpenseTrackerComponent implements OnInit {
  private ledgerService = inject(LedgerService); 

  activeType = signal<TrackerType>('expense');
  isEditing = signal<boolean>(false);
  editingId = signal<number | null>(null); 

  categoriesMap = signal<{ [key in TrackerType]: string[] }>({
    expense: ['Food', 'Rent', 'Utilities', 'Entertainment'],
    asset: ['Cash', 'Stocks', 'Real Estate', 'Crypto'],
    liability: ['Credit Card', 'Mortgage', 'Student Loan']
  });

  newCategoryName = '';
  showCustomInput = false;

  currentCategories = computed(() => this.categoriesMap()[this.activeType()]);
  items = this.ledgerService.items; 

  // Updated Portfolio math to reflect your HTML template logic
  netBalance = computed(() => {
    return this.items().reduce((total, item) => {
      return item.type === 'asset' ? total + item.amount : total - item.amount;
    }, 0);
  });

  formData = {
    title: '',
    amount: 0,
    category: 'Food'
  };

  ngOnInit() {
    this.ledgerService.fetchItems().subscribe();
  }

  changeType(type: TrackerType) {
    this.activeType.set(type);
    this.formData.category = this.categoriesMap()[type][0];
    this.showCustomInput = false; 
  }

  addCustomCategory() {
    const trimmed = this.newCategoryName.trim();
    if (!trimmed) return;

    const formattedCategory = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
    const currentMap = this.categoriesMap();
    const currentType = this.activeType();

    if (!currentMap[currentType].includes(formattedCategory)) {
      this.categoriesMap.update(prev => ({
        ...prev,
        [currentType]: [...prev[currentType], formattedCategory]
      }));
    }

    this.formData.category = formattedCategory;
    this.newCategoryName = '';
    this.showCustomInput = false;
  }

saveItem() {
  const payload: TrackerItem = {
    amount: this.formData.amount,
    type: this.activeType(),
    category: this.formData.category,
    description: this.formData.title,
    
    transaction_date: new Date().toISOString().split('T')[0] 
  };

  if (this.isEditing() && this.editingId() !== null) {
    this.ledgerService.updateItem(this.editingId()!, payload).subscribe({
      next: () => this.resetForm(),
      error: (err) => console.error('Failed to update record:', err)
    });
  } else {
    this.ledgerService.addItem(payload).subscribe({
      next: () => this.resetForm(),
      error: (err) => console.error('Failed to add record:', err)
    });
  }
}

  editItem(item: TrackerItem) {
    this.isEditing.set(true);
    this.editingId.set(item.id || null);
    this.activeType.set(item.type);
    this.formData = {
      title: item.description,
      amount: item.amount,
      category: item.category
    };
  }

  deleteItem(id: number | undefined) {
    if (id === undefined) return;
    if (confirm('Are you sure you want to delete this record?')) {
      this.ledgerService.deleteItem(id).subscribe({
        next: () => {
          if (this.editingId() === id) this.resetForm();
        },
        error: (err) => console.error('Failed to delete transaction:', err)
      });
    }
  }

  resetForm() {
    this.isEditing.set(false);
    this.editingId.set(null);
    this.formData = { 
      title: '', 
      amount: 0, 
      category: this.categoriesMap()[this.activeType()][0]
    };
  }
}